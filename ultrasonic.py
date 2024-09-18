import RPi.GPIO as GPIO
import time

# Setup
TRIG = 23  # GPIO pin for the Trigger
ECHO = 24  # GPIO pin for the Echo

# Set GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def distance():
    # Ensure the trigger pin is low
    GPIO.output(TRIG, GPIO.LOW)
    time.sleep(2)

    # Send a 10us pulse to trigger the sensor
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)  # 10 microseconds
    GPIO.output(TRIG, GPIO.LOW)

    # Measure the time taken for the echo to return
    while GPIO.input(ECHO) == GPIO.LOW:
        pulse_start = time.time()
    
    while GPIO.input(ECHO) == GPIO.HIGH:
        pulse_end = time.time()

    # Calculate the distance
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 34300 / 2  # Speed of sound is 34300 cm/s

    return distance

try:
    while True:
        dist = distance()
        US_Distance = print(f"Distance: {dist:.2f} cm")
        time.sleep(1)  # Delay between measurements

except KeyboardInterrupt:
    print("Program stopped by user")
finally:
    GPIO.cleanup()
