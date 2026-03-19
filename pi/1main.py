import time
from camera_module import take_photo
from image_processing import process_image

TOTAL_IMAGES = 16
GROUP_SIZE = 4

SHORT_INTERVAL = 5   # seconds between images
LONG_INTERVAL = 30   # seconds between craters

CRATER_NAMES = ["Crater1", "Crater2", "Crater3", "Crater4"]

def main():
    print("Starting CubeSat capture mission...\n")

    crater_index = 0

    for i in range(TOTAL_IMAGES):
        crater_id = CRATER_NAMES[crater_index]

        print(f"Taking image {i+1}/{TOTAL_IMAGES} for {crater_id}")

        # Pass crater_id to camera_module
        img_path = take_photo(crater_id=crater_id)

        process_image(img_path)

        print("Cycle complete\n")

        # Switch crater after GROUP_SIZE images
        if (i + 1) % GROUP_SIZE == 0:
            crater_index += 1
            if crater_index < len(CRATER_NAMES):
                print(f"Switching to next crater... waiting {LONG_INTERVAL} seconds\n")
                time.sleep(LONG_INTERVAL)
        else:
            time.sleep(SHORT_INTERVAL)

    print("Mission complete.")

if __name__ == "__main__":
    main()