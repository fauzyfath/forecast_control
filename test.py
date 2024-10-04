import time
import serial
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress, XBeeNetwork

# Configure your local XBee
PORT = "/dev/ttyUSB0"  # Update with your correct port
BAUD_RATE = 9600       # Baud rate for XBee communication

# Define the address of the remote XBee
REMOTE_XBEE_ADDRESS = "0013A2004213D0CD"  # Replace with your remote XBee's 64-bit address

# Initialize local XBee device
device = XBeeDevice(PORT, BAUD_RATE)

def send_message_to_remote(data):
    try:
        device.open()

        # Create a Remote XBee object (specify the 64-bit address of the target XBee)
        remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string(REMOTE_XBEE_ADDRESS))

        # Send the message to the remote XBee
        device.send_data(remote_device, data)
        print(f"Message sent: {data}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if device.is_open():
            device.close()

def receive_message():
    try:
        device.open()

        print("Waiting for data from remote XBee...")
        while True:
            # Wait for incoming data
            xbee_message = device.read_data()
            if xbee_message:
                received_data = xbee_message.data.decode("utf-8")
                print(f"Message received: {received_data}")

                # You can also print the sender's 64-bit address if needed
                sender_address = xbee_message.remote_device.get_64bit_addr()
                print(f"Message from: {sender_address}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if device.is_open():
            device.close()

if __name__ == "__main__":
    try:
        # Example: Sending data
        message_to_send = "Hello from local XBee!"
        send_message_to_remote(message_to_send)

        # Example: Receiving data (continuously listens for incoming messages)
        receive_message()

    except KeyboardInterrupt:
        print("Program interrupted by user.")

    finally:
        if device.is_open():
            device.close()
