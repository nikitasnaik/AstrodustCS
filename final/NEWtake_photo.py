import os
from datetime import datetime
from picamera2 import Picamera2
import time

# Initialize camera once
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()

# Give camera time to warm up
time.sleep(2)


def take_photo(crater_id):
    """
    Takes a photo and saves it into:
    images/<crater_id>/
    Returns full image path.
    """

    # --- Create folder structure inside repo ---
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(base_dir, "images", crater_id)
    os.makedirs(image_dir, exist_ok=True)

    # --- Create filename with timestamp ---
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{crater_id}_{timestamp}.jpg"
    img_path = os.path.join(image_dir, filename)

    # --- Capture image ---
    picam2.capture_file(img_path)

    print(f"[CAMERA] Saved image: {img_path}")

    return img_path


# def take_photo():
#     """
#     Automatically takes a photo every 5 seconds and saves
#     it to the SAME location as defined by REPO_PATH + FOLDER_PATH
#     """

#     print("Starting automatic capture every 5 seconds...")

#     picam2.start()  # start camera once

#     while True:
#         name = "TeamAstrodust"
#         img_path = img_gen(name)

#         picam2.capture_file(img_path)
#         print(f"Photo saved: {img_path}")

#         # OPTIONAL: push to GitHub
#         # git_push()

#         time.sleep(5)