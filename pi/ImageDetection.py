import cv2
import numpy as np

image = cv2.imread("moon_image.jpg")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

<<<<<<< HEAD
=======
gray = cv2.GaussianBlur(gray, (5,5), 0)  # smooth small variations

>>>>>>> nikita
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

<<<<<<< HEAD
rim_brightness = np.mean(rim_pixels)

print("Rim brightness:", rim_brightness)

brightness_values = [142, 145, 143, 141, 144]
mean_brightness = np.mean(brightness_values)
constancy = np.std(brightness_values)
=======
hist = cv2.calcHist([rim_pixels.astype(np.uint8)], [0], None, [256], [0,256])
# Optional: compute a uniformity metric, e.g., std deviation
rim_uniformity = np.std(rim_pixels)
print("Rim uniformity (std dev):", rim_uniformity)

brightness_threshold = 200  # example threshold
illuminated_count = np.sum(rim_pixels > brightness_threshold)
percent_illuminated = (illuminated_count / len(rim_pixels)) * 100

rim_brightness = np.mean(rim_pixels)

print("Rim brightness:", rim_brightness)
print("Percent illuminated pixels:", percent_illuminated)

# brightness_values = [142, 145, 143, 141, 144]
# mean_brightness = np.mean(brightness_values)
# constancy = np.std(brightness_values)


brightness_values = []
percent_illuminated_values = []

image_files = ["moon1.jpg", "moon2.jpg", "moon3.jpg"]  # list of images

for file in image_files:
    image = cv2.imread(file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5,5), 0)
    
    # repeat your masking code to get rim_mask
    # ...
    
    rim_pixels = gray[rim_mask == 255]
    brightness_values.append(np.mean(rim_pixels))
    percent_illuminated_values.append(np.sum(rim_pixels > brightness_threshold) / len(rim_pixels) * 100)

mean_brightness = np.mean(brightness_values)
constancy = np.std(brightness_values)
print("Mean brightness over time:", mean_brightness)
print("Constancy (std dev):", constancy)
>>>>>>> nikita
