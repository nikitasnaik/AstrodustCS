import time
from camera_module import take_photo
from image_processing import process_image
import numpy as np

TOTAL_IMAGES = 16
GROUP_SIZE = 4
SHORT_INTERVAL = 5
LONG_INTERVAL = 20
CRATER_NAMES = ["Crater1", "Crater2", "Crater3", "Crater4"]

# Store bright rim brightness values per crater
crater_data = {crater: [] for crater in CRATER_NAMES}

def main():
    print("Starting CubeSat mission...\n")
    crater_index = 0

    for i in range(TOTAL_IMAGES):
        crater_id = CRATER_NAMES[crater_index]
        print(f"Taking image {i+1}/{TOTAL_IMAGES} for {crater_id}")

        img_path = take_photo(crater_id=crater_id)
        print("Photo saved")

        avg_brightness = process_image(img_path)
        crater_data[crater_id].append(avg_brightness)

        print("Cycle complete\n")

        # Switch crater after 4 images
        if (i+1) % GROUP_SIZE == 0:
            crater_index += 1
            if crater_index < len(CRATER_NAMES):
                print(f"Switching to next crater... waiting {LONG_INTERVAL} seconds\n")
                time.sleep(LONG_INTERVAL)
        else:
            time.sleep(SHORT_INTERVAL)

    # --- Analyze crater statistics ---
    print("\n--- Crater Brightness Summary ---")
    best_score = -1
    best_crater = None
    for crater, values in crater_data.items():
        avg = np.mean(values)
        consistency = np.std(values)
        print(f"{crater}: Average Bright Rim = {avg:.2f}, Consistency = {consistency:.2f}")
        score = avg / (1 + consistency)  # Higher average + lower std = better
        if score > best_score:
            best_score = score
            best_crater = crater

    print(f"\nBest crater (brightest & most consistent): {best_crater}")
    print("Mission complete.")

if __name__ == "__main__":
    main()