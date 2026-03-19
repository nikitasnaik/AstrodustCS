import cv2
import numpy as np
import os

def process_image(file):
    image = cv2.imread(file)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5,5), 0)

    # Save grayscale image alongside original
    gray_filename = os.path.join(
        os.path.dirname(file), 
        "gray_" + os.path.basename(file)
    )
    cv2.imwrite(gray_filename, gray)
    print(f"Grayscale image saved: {gray_filename}")

    threshold_value = 30
    _, shadow_mask = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(shadow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        print("No contours found")
        return

    largest_psr = max(contours, key=cv2.contourArea)

    psr_mask = np.zeros_like(gray)
    cv2.drawContours(psr_mask, [largest_psr], -1, 255, -1)

    kernel = np.ones((15,15), np.uint8)
    expanded_mask = cv2.dilate(psr_mask, kernel, iterations=1)

    rim_mask = cv2.subtract(expanded_mask, psr_mask)
    rim_pixels = gray[rim_mask == 255]

    if len(rim_pixels) == 0:
        print("No rim pixels")
        return

    brightness_threshold = 200
    rim_brightness = np.mean(rim_pixels)
    percent_illuminated = np.sum(rim_pixels > brightness_threshold) / len(rim_pixels) * 100
    rim_uniformity = np.std(rim_pixels)

    print("Rim brightness:", rim_brightness)
    print("Percent illuminated:", percent_illuminated)
    print("Uniformity:", rim_uniformity)