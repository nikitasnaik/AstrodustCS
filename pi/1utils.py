import os
from datetime import datetime

# Folder you can access easily
SAVE_DIR = "/home/pi/MissionImages"

# Create folder if it doesn't exist
os.makedirs(SAVE_DIR, exist_ok=True)

def img_gen(name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.jpg"
    return os.path.join(SAVE_DIR, filename)