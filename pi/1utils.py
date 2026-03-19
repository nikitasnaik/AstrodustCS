import os
from datetime import datetime

BASE_DIR = "/home/pi/MissionImages"

# Ensure base directory exists
os.makedirs(BASE_DIR, exist_ok=True)

def img_gen(name, crater_id="Crater1"):
    # Create folder for this crater
    folder_path = os.path.join(BASE_DIR, crater_id)
    os.makedirs(folder_path, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.jpg"
    return os.path.join(folder_path, filename)