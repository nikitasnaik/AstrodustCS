import time
import os
import numpy as np

from camera_module import take_photo
from image_processing import process_image
from git_upload import git_push

TOTAL_IMAGES = 16
GROUP_SIZE = 4
SHORT_INTERVAL = 5
LONG_INTERVAL = 20
CRATER_NAMES = ["Crater1", "Crater2", "Crater3", "Crater4"]

# Store bright rim brightness values per crater
crater_data = {crater: [] for crater in CRATER_NAMES}


def save_crater_summary(crater_id, values):
    """
    Saves a summary.txt file inside the crater folder.
    """
    folder_path = os.path.join("/home/pi/MissionImages", crater_id)
    summary_path = os.path.join(folder_path, "summary.txt")

    avg = np.mean(values)
    std = np.std(values)

    with open(summary_path, "w") as f:
        f.write(f"Crater: {crater_id}\n")
        f.write(f"Number of Images: {len(values)}\n\n")

        f.write("Individual Brightness Values:\n")
        for i, val in enumerate(values, 1):
            f.write(f"Image {i}: {val:.2f}\n")

        f.write("\n")
        f.write(f"Average Brightness: {avg:.2f}\n")
        f.write(f"Consistency (Std Dev): {std:.2f}\n")

    print(f"Summary saved for {crater_id}")


def main():
    print("Starting CubeSat mission...\n")
    crater_index = 0

    for i in range(TOTAL_IMAGES):
        crater_id = CRATER_NAMES[crater_index]
        print(f"Taking image {i+1}/{TOTAL_IMAGES} for {crater_id}")

        # Take photo
        img_path = take_photo(crater_id=crater_id)

        # Process image
        avg_brightness = process_image(img_path)
        crater_data[crater_id].append(avg_brightness)

        print("Cycle complete\n")

        # --- After every 4 images (one crater batch) ---
        if (i + 1) % GROUP_SIZE == 0:
            # Save summary for this crater
            save_crater_summary(crater_id, crater_data[crater_id])

            # Push images + summary to GitHub
            print(f"Pushing images + results for {crater_id} to GitHub...\n")
            git_push(crater_id)

            crater_index += 1

            # Wait before switching to next crater
            if crater_index < len(CRATER_NAMES):
                print(f"Switching to next crater... waiting {LONG_INTERVAL} seconds\n")
                time.sleep(LONG_INTERVAL)
        else:
            time.sleep(SHORT_INTERVAL)

    # --- Final mission summary ---
    print("\n--- Crater Brightness Summary ---")
    best_score = -1
    best_crater = None

    for crater, values in crater_data.items():
        avg = np.mean(values)
        consistency = np.std(values)

        print(f"{crater}: Average Bright Rim = {avg:.2f}, Consistency = {consistency:.2f}")

        score = avg / (1 + consistency)
        if score > best_score:
            best_score = score
            best_crater = crater

    print(f"\nBest crater (brightest & most consistent): {best_crater}")
    print("Mission complete.")


if __name__ == "__main__":
    main()