import time
import os
import numpy as np
from datetime import datetime

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

# Mission log file
LOG_FILE = "/home/pi/MissionImages/mission_log.txt"


def log_event(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")


def save_crater_summary(crater_id, values):
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

    log_event(f"SUMMARY — {crater_id} Avg: {avg:.2f} | Consistency: {std:.2f}")


def main():
    log_event("MISSION START — Team Astrodust CubeSat")

    crater_index = 0

    for i in range(TOTAL_IMAGES):
        crater_id = CRATER_NAMES[crater_index]
        img_num = len(crater_data[crater_id]) + 1

        log_event(f"CAPTURE — Taking {crater_id} Image {img_num}")

        # Take photo
        img_path = take_photo(crater_id=crater_id)
        log_event(f"CAPTURE — Saved {img_path}")

        # Process image
        avg_brightness = process_image(img_path)
        crater_data[crater_id].append(avg_brightness)

        log_event(f"PROCESS — {crater_id} Image {img_num} Brightness: {avg_brightness:.2f}")

        # --- After every 4 images (one crater batch) ---
        if (i + 1) % GROUP_SIZE == 0:
            # Save summary
            save_crater_summary(crater_id, crater_data[crater_id])

            # Push to GitHub
            log_event(f"DOWNLINK — Pushing {crater_id} batch to GitHub")
            git_push(crater_id)

            crater_index += 1

            if crater_index < len(CRATER_NAMES):
                log_event(f"WAIT — Switching crater, sleeping {LONG_INTERVAL}s")
                time.sleep(LONG_INTERVAL)
        else:
            time.sleep(SHORT_INTERVAL)

    # --- Final mission summary ---
    log_event("FINAL ANALYSIS — Computing best crater")

    best_score = -1
    best_crater = None

    for crater, values in crater_data.items():
        avg = np.mean(values)
        consistency = np.std(values)

        log_event(f"RESULT — {crater}: Avg={avg:.2f}, Consistency={consistency:.2f}")

        score = avg / (1 + consistency)
        if score > best_score:
            best_score = score
            best_crater = crater

    log_event(f"MISSION RESULT — Best crater: {best_crater}")
    log_event("MISSION COMPLETE")


if __name__ == "__main__":
    main()