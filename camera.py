from picamera import PiCamera
from time import sleep
from datetime import datetime
import os

camera = PiCamera()

def capture_image(directory='/images'):
    try:
        # Ensure the directory exists
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Generate the filename based on the current date
        date_str = datetime.now().strftime('%Y-%m-%d')
        image_filename = f"{directory}/{date_str}.jpg"
        
        # Start the camera preview (optional, for display)
        camera.start_preview()
        # Give some time for the camera to adjust to lighting conditions
        sleep(2)

        # Capture the image and save it to the specified path
        camera.capture(image_filename)
        print(f"Image captured and saved to {image_filename}")
    
    finally:
        # Stop the camera preview
        camera.stop_preview()
        # Close the camera to release the resource
        camera.close()
