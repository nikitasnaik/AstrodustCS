import time
from picamera2 import Picamera2
from utils import img_gen

picam2 = Picamera2()
picam2.start()

def take_photo():
    time.sleep(1)  # small buffer

    name = "TeamAstrodust"
    img_path = img_gen(name)

    picam2.capture_file(img_path)

    print(f"Photo saved: {img_path}")

    return img_path