import time
from picamera2 import Picamera2
from utils import img_gen

picam2 = Picamera2()
picam2.start()

def take_photo(crater_id="Crater1"):
    time.sleep(1)  # small buffer

    name = "TeamAstrodust"
    img_path = img_gen(name, crater_id=crater_id)

    picam2.capture_file(img_path)
    print(f"Photo saved: {img_path}")
    return img_path