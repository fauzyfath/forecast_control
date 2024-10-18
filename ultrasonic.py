from gpiozero import DistanceSensor, Device
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import RPi.GPIO as GPIO
import warnings

# Suppress specific warnings related to no echo
warnings.filterwarnings("ignore", category=UserWarning, module='gpiozero.input_devices')

# Use the pigpio library for accurate timing
factory = PiGPIOFactory()

# Initialize DistanceSensor with retries and a timeout to handle "no echo" warnings gracefully
sensor = DistanceSensor(
    echo=23, 
    trigger=24, 
    max_distance=4,  # Maximum range of the sensor (in meters)
    threshold_distance=0.05,  # Optional: Trigger when distance falls below this value
    pin_factory=factory
)

# Global variable to store the distance data
distance = 0.0

# Function to get the distance data
def get_distance_data():
    global distance
    return {"distance": distance}

# Function to handle the distance sensor logic and retry mechanism
def run_ultrasonic():
    global distance
    try:
        print("Ultrasonic Measurement started...")
        sleep(0.5)  # Allow the module to settle

        while True:
            try:
                # Measure the current distance (in cm)
                measured_distance = sensor.distance * 100  # Convert to cm

                if measured_distance > 400:  # Handle out-of-range readings
                    print("Warning: Distance out of range or no object detected")
                    measured_distance = 100.0  # Set to default 100 cm for invalid readings

                distance = round(measured_distance, 2)  # Round to 2 decimal places
                print(f"Distance: {distance:.2f} cm")
            except Exception as e:
                print(f"Error reading distance: {e}")
                distance = 0.0  # Reset to 0 if reading fails

            sleep(1)  # Adjust delay based on your needs

    except KeyboardInterrupt:
        print("Ultrasonic sensor measurement stopped by user.")

    finally:
        sensor.close()  # Clean up the sensor
        GPIO.cleanup()  # Reset GPIO settings
        print("Sensor resources released.")

# For standalone testing
if __name__ == "__main__":
    run_ultrasonic()
