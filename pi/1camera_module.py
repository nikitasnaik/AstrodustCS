import time
from camera_module import take_photo
from image_processing import process_image

TOTAL_IMAGES = 16
GROUP_SIZE = 4

SHORT_INTERVAL = 5   # between images
LONG_INTERVAL = 30   # between groups

def main():
    print("Starting CubeSat capture mission...\n")

    for i in range(TOTAL_IMAGES):
        print(f"Taking image {i+1}/{TOTAL_IMAGES}")

        img_path = take_photo()
        process_image(img_path)

        # Decide timing
        if (i + 1) % GROUP_SIZE == 0 and i != TOTAL_IMAGES - 1:
            print("Switching crater... waiting 30 seconds\n")
            time.sleep(LONG_INTERVAL)
        else:
            time.sleep(SHORT_INTERVAL)

    print("Mission complete.")

if __name__ == "__main__":
    main()