from picamera2 import Picamera2, Preview
import time
from datetime import datetime

def capture_image():
    # Initialize the camera
    camera = Picamera2()
    
    # Configure the camera for still capture
    camera.configure(camera.still_configuration)
    
    # Start the camera preview (optional)
    camera.start_preview(Preview.QTGL)
    
    # Allow the camera to warm up
    time.sleep(2)
    
    # Start the camera
    camera.start()
    
    # Get today's date and format it as YYYY-MM-DD_HH-MM-SS for a unique file name
    today_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Create the full file path with today's date as the file name
    file_path = f"/home/admin/Desktop/forecast_control/images/{today_date}.jpg"
    
    # Capture an image and save it
    camera.capture_file(file_path)
    print(f"Image captured and saved as {file_path}")
    
    # Return the image file path
    return file_path

if __name__ == "__main__":
    capture_image()
