import time
import threading
from rainGauge import run_rain_gauge, get_rainfall_data
from anonemeter import run_anonemeter, get_wind_data
from ultrasonic import run_ultrasonic, get_distance_data
from BH1750 import run_bh1750, get_light_data
from camera import capture_image
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress
from threading import Lock

# Configure your local XBee
PORT = "/dev/ttyUSB0"  # Update with your correct port
BAUD_RATE = 9600       # Baud rate for XBee communication
REMOTE_XBEE_ADDRESS = "0013A2004213D0CD"  # Replace with your remote XBee's 64-bit address

# Initialize local XBee device
device = XBeeDevice(PORT, BAUD_RATE)
device_lock = Lock()  # Lock for thread-safe device communication

# Function to send a message to the remote XBee
def send_message_to_remote(data, current_time):
    message = f"time: {current_time} data: {data}"
    try:
        with device_lock:
            if not device.is_open():
                device.open()

            # Create a Remote XBee object (specify the 64-bit address of the target XBee)
            remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string(REMOTE_XBEE_ADDRESS))
            
            # Send the message to the remote XBee
            time.sleep(2)
            device.send_data(remote_device, message)
            print(f"Data sent: {message}")

    except Exception as e:
        print(f"Error: {e}")

# Function to receive messages from the remote XBee
def receive_message():
    try:
        with device_lock:
            if not device.is_open():
                device.open()

        while True:
            # Wait for incoming data
            xbee_message = device.read_data()
            if xbee_message:
                received_data = xbee_message.data.decode("utf-8")
                print(f"Message received: {received_data}")

                # You can also print the sender's 64-bit address if needed
                sender_address = xbee_message.remote_device.get_64bit_addr()
                print(f"Message from: {sender_address}")

                # Check if the action is "activate"
                if received_data.lower() == "activate":
                    print("Activation command received. Capturing image...")
                    image_path = capture_image()  # Capture image and get the image path
                    
                    # Send the image path via Zigbee
                    send_image_path(image_path)

    except Exception as e:
        print(f"Error: {e}")

# Function to send the image path after capturing
def send_image_path(image_path):
    path = image_path
    try:
        with device_lock:
            if not device.is_open():
                device.open()

            # Create a Remote XBee object (specify the 64-bit address of the target XBee)
            remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string(REMOTE_XBEE_ADDRESS))
            
            # Send the image path to the remote XBee
            time.sleep(2)
            device.send_data(remote_device, path)
            print(f"Image path sent: {path}")

    except Exception as e:
        print(f"Error: {e}")

# Function to run the rain gauge thread
def run_rain_gauge_thread():
    try:
        run_rain_gauge()
    except Exception as e:
        print(f"Error in rain gauge thread: {e}")

# Function to run the anemometer thread
def run_anemometer_thread():
    try:
        run_anonemeter()
    except Exception as e:
        print(f"Error in anemometer thread: {e}")

# Function to run the ultrasonic sensor thread
def run_ultrasonic_thread():
    try:
        run_ultrasonic()
    except Exception as e:
        print(f"Error in ultrasonic thread: {e}")

# Function to run the BH1750 light sensor thread
def run_bh1750_thread():
    try:
        run_bh1750()
    except Exception as e:
        print(f"Error in BH1750 thread: {e}")

# Main function to handle sensor data collection and communication
if __name__ == "__main__":
    try:
        # Start all sensors in separate threads
        gauge_thread = threading.Thread(target=run_rain_gauge_thread, daemon=True)
        gauge_thread.start()

        anemometer_thread = threading.Thread(target=run_anemometer_thread, daemon=True)
        anemometer_thread.start()

        bh1750_thread = threading.Thread(target=run_bh1750_thread, daemon=True)
        bh1750_thread.start()

        ultrasonic_thread = threading.Thread(target=run_ultrasonic_thread, daemon=True)
        ultrasonic_thread.start()

        # Start Zigbee receiver in a separate thread
        zigbee_thread = threading.Thread(target=receive_message, daemon=True)
        zigbee_thread.start()

        # Main loop to collect sensor data and send messages
        while True:
            # Get data from all sensors
            rain_data = get_rainfall_data()
            wind_data = get_wind_data()
            distance_data = get_distance_data()
            light_data = get_light_data()

            # Combine all data into one variable (string)
            current_data = f"Rainfall:{rain_data}, Wind:{wind_data}, Distance:{distance_data}, Light:{light_data}"

            # Get the current time in seconds since the epoch
            current_time = time.time()
            
            # Convert it to a readable format
            local_time = time.localtime(current_time)
            formatted_time = time.strftime("%H:%M:%S", local_time)
            
            # Print the current time and data
            print(f"Current time: {formatted_time}")
            print(current_data)
            
            # Send data via Zigbee
            send_message_to_remote(current_data, formatted_time)
            
            time.sleep(10)  # Adjust sleep time as needed

    except KeyboardInterrupt:
        print('System stopped by user.')
    finally:
        with device_lock:
            if device.is_open():
                device.close()
        print('Cleaning up resources.')
