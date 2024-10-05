import serial
import time
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress, XBeeNetwork

port = "/dev/ttyUSB0"
Baud_rate = 9600

remote_xbee_address = "0013A2004213D0CD"

device = XBeeDevice(port, Baud_rate)

def send_message_to_remote(data):
    try:
        device.open()

        remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string(remote_xbee_address))
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
            xbee_message = device.read_data()
            if xbee_message:
                received_data = xbee_message.data.decode("utf-8")
                print(f"Message received: {received_data}")

                sender_address = xbee_message.remote_device.get_64bit_addr()
                print(f"Message from: {sender_address}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if device.is_open():
            device.close()

if __name__ == "__main__":
    try:
        # Start the message sending loop
        while True:
            message_to_send = input("Enter message to send (or 'exit' to quit): ")
            if message_to_send.lower() == 'exit':
                print("Exiting message sending loop.")
                break
            send_message_to_remote(message_to_send)

        # Start receiving messages
        receive_message()

    except KeyboardInterrupt:
        print("Program interrupted by user.")
    
    finally:
        if device.is_open():
            device.close()