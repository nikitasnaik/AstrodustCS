import cv2
import numpy as np

image = cv2.imread("moon_image.jpg")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

threshold_value = 30
_, shadow_mask = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY_INV)

contours, _ = cv2.findContours(shadow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

largest_psr = max(contours, key=cv2.contourArea)

psr_mask = np.zeros_like(gray)
cv2.drawContours(psr_mask, [largest_psr], -1, 255, -1)

kernel = np.ones((15,15), np.uint8)
expanded_mask = cv2.dilate(psr_mask, kernel, iterations=1)

rim_mask = cv2.subtract(expanded_mask, psr_mask)

rim_pixels = gray[rim_mask == 255]

rim_brightness = np.mean(rim_pixels)

print("Rim brightness:", rim_brightness)

brightness_values = [142, 145, 143, 141, 144]
mean_brightness = np.mean(brightness_values)
constancy = np.std(brightness_values)