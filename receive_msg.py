import threading
import time
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

# Function to send image path to the remote XBee
def send_image_path(image_path):
    try:
        with device_lock:
            if not device.is_open():
                device.open()

            # Create a remote XBee device object
            remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string(REMOTE_XBEE_ADDRESS))

            # Send the image path as a message to the remote XBee
            time.sleep(2)  # Optional delay before sending
            device.send_data(remote_device, image_path)
            print(f"Image path sent: {image_path}")

    except Exception as e:
        print(f"Error sending image path: {e}")

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
        print(f"Error receiving message: {e}")

if __name__ == "__main__":
    try:
        # Start Zigbee receiver in a separate thread
        zigbee_thread = threading.Thread(target=receive_message, daemon=True)
        zigbee_thread.start()

        # Main loop (acts as a heartbeat or keeps the main thread alive)
        while True:
            time.sleep(10)  # Adjust sleep time as needed

    except KeyboardInterrupt:
        print('System stopped by user.')
    finally:
        with device_lock:
            if device.is_open():
                device.close()
        print('Cleaning up resources.')
