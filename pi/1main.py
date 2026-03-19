import time
from camera_module import take_photo
from image_processing import process_image

INTERVAL = 5  # seconds

def main():
    print("Starting automatic image capture every 5 seconds...")

    while True:
        img_path = take_photo()

        process_image(img_path)

        print("Cycle complete\n")

        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()