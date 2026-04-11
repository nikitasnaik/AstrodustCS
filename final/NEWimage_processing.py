import cv2
import numpy as np
import os

def process_image(file):
    """
    Processes the image:
    - Saves grayscale image
    - Detects brightest rim pixels dynamically
    - Prints helpful messages about detection
    - Prints average and maximum bright rim brightness
    - Returns average bright rim brightness
    """
    image = cv2.imread(file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Reduced blur to preserve bright pixels
    gray = cv2.GaussianBlur(gray, (3,3), 0)

    # Save grayscale image
    gray_filename = os.path.join(os.path.dirname(file), "gray_" + os.path.basename(file))
    cv2.imwrite(gray_filename, gray)
    print("Grayscale image saved")

    # Threshold to find shadow (dark crater interior)
    _, shadow_mask = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(shadow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        print("No contours found")
        return 0

    largest_psr = max(contours, key=cv2.contourArea)
    psr_mask = np.zeros_like(gray)
    cv2.drawContours(psr_mask, [largest_psr], -1, 255, -1)

    # Create rim mask
    kernel = np.ones((15,15), np.uint8)
    expanded_mask = cv2.dilate(psr_mask, kernel, iterations=1)
    rim_mask = cv2.subtract(expanded_mask, psr_mask)
    rim_pixels = gray[rim_mask == 255]

    if len(rim_pixels) == 0:
        print("No rim pixels found")
        return 0

    # Dynamic threshold: top 30% of rim brightness
    max_pixel = np.max(rim_pixels)
    threshold = max_pixel * 0.7
    bright_rim_pixels = rim_pixels[rim_pixels > threshold]

    if len(bright_rim_pixels) == 0:
        print("No bright rim pixels found, using all rim pixels")
        bright_rim_pixels = rim_pixels  # fallback

    avg_brightness = np.mean(bright_rim_pixels)
    max_brightness = np.max(bright_rim_pixels)
    std_brightness = np.std(bright_rim_pixels)

    print(f"Bright rim avg: {avg_brightness:.2f}, max: {max_brightness:.2f}, consistency: {std_brightness:.2f}")

    return avg_brightness