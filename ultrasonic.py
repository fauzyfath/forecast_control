import RPi.GPIO as GPIO
from time import sleep, time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up the ultrasonic sensor pins
TRIG = 23  # GPIO pin connected to Trigger pin of the sensor
ECHO = 24  # GPIO pin connected to Echo pin of the sensor

# Set up GPIO pins as input/output
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

distance = 0  # Variable to store distance

# Function to get distance from ultrasonic sensor
def get_distance_data():
    global distance
    return {
        "distance": distance
    }

# Function to run the ultrasonic sensor and measure distance
def run_ultrasonic():
    global distance
    try:
        while True:
            # Ensure the trigger pin is low
            GPIO.output(TRIG, False)
            sleep(0.1)

            # Generate a 10µs pulse to trigger the sensor
            GPIO.output(TRIG, True)
            sleep(0.00001)  # 10 microseconds
            GPIO.output(TRIG, False)

            # Measure the time between sending and receiving the pulse
            while GPIO.input(ECHO) == 0:
                pulse_start = time()

            while GPIO.input(ECHO) == 1:
                pulse_end = time()

            pulse_duration = pulse_end - pulse_start

            # Calculate distance (speed of sound is 34300 cm/s)
            distance = pulse_duration * 17150
            distance = round(distance, 2)

            print(f"Distance: {distance} cm")
            sleep(1)

    except KeyboardInterrupt:
        print("Measurement stopped by User")

    finally:
        GPIO.cleanup()  # Clean up GP
