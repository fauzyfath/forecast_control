# import time
# # import RPi.GPIO as GPIO
# # from VEML6030py.veml6030 import VEML6030
 
import time
import smbus2
from gpiozero import DistanceSensor, LightSensor

# Setup
bus = smbus2.SMBus(1)
ultraSonic = DistanceSensor(echo=23, trigger=24)
lightsensor = LightSensor


def check_distance():
    distance = ultraSonic.distance
    print(f'Distance = {distance:.2f} meters')

    if distance < 0.5:
        print("Object detected within 0.5 meters!")
    else:
        print("No object detected within 0.5 meters.")

# Main function
if __name__ == "__main__":
    try:
        while True:
            check_distance()
            time.sleep(0.5)  

    except KeyboardInterrupt:
        print('System stopped by user.')
    finally:
        print('Cleaning up resources.')
        # Add any necessary cleanup code here
