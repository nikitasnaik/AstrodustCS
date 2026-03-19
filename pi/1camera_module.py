import time
from picamera2 import Picamera2
from utils import img_gen  # keep your existing utils for naming

# Initialize camera
picam2 = Picamera2()

# --- MANUAL SETTINGS ---
# Disable auto-exposure and auto-gain for reliable brightness measurements
picam2.set_controls({
    "AeEnable": False,        # turn off auto-exposure
    "AnalogueGain": 2.0,      # adjust as needed (1.0–4.0)
    "ExposureTime": 30000     # in microseconds; adjust for brightness
})
picam2.start()


def take_photo(crater_id="Crater"):
    """
    Captures an image and saves it to a folder for the crater.
    Returns the image path.
    """
    time.sleep(1)  # small buffer for camera to stabilize

    # Generate image file path using utils
    name = "TeamAstrodust"
    img_path = img_gen(name, crater_id=crater_id)

    picam2.capture_file(img_path)

    print("Photo saved")
    return img_path