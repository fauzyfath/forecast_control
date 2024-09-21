from gpiozero import DistanceSensor
from time import sleep

# Set up the ultrasonic sensor
sensor = DistanceSensor(echo=24, trigger=23)
distance = 0

def get_distance_data():
    return{
        "distance:": distance
    }

def run_ultrasonic():
    global sensor
    global distance
    try:
        while True:
            distance = sensor.distance * 100  # Convert to cm
            sleep(1)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
