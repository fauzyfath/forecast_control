import time
import threading
from rainGauge import run_rain_gauge, get_rainfall_data
from anonemeter import run_anonemeter, get_wind_data
from ultrasonic import run_ultrasonic, get_distance_data
from BH1750 import run_bh1750, get_light_data
from receive_msg import receive_message, send_image_path
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
    try:
        with device_lock:
            if not device.is_open():
                device.open()

            remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string(REMOTE_XBEE_ADDRESS))
            msg = f"{current_time},{data}"
            # Send the message to the remote XBee
            time.sleep(2)
            device.send_data(remote_device, msg)
            print(f"Data sent: {msg}")

    except Exception as e:
        print(f"Error sending Zigbee message: {e}")
    
# Function to format and compress the sensor data
def format_data(rain_data, wind_data, distance_data, light_data):
    # Use abbreviations for weather and add light descriptions
    rain_weather_map = {
        "Berawan": "(B)",
        "Hujan Ringan": "(HR)",
        "Hujan Sedang": "(HS)",
        "Hujan Lebat": "(HL)",
        "Hujan Extreme": "(HE)",
    }
    light_weather_map = {
        "Mendung": "(M)",
        "Cerah": "(C)",
        "Malam/Hujan": "(M/H)",
        "Error reading light level": "(ER)",
    }   
    
    # Rain data
    rain_condition = rain_weather_map.get(rain_data['cuaca'], "N/A")  # Default to N/A if not found
    rain = f"{rain_data['jumlah_tip']},{rain_data['curah_hujan_per_menit']:.1f},{rain_data['curah_hujan_per_jam']:.1f},{rain_data['curah_hujan_per_hari']:.1f},{rain_data['curah_hujan_hari_ini']:.1f},{rain_condition}"
    
    # Wind data
    wind = f"{wind_data['rotasi_per_detik']:.1f},{wind_data['kecepatan_meter_per_detik']:.1f},{wind_data['kecepatan_kilometer_per_jam']:.1f}"
    
    # Distance data
    distance = f"{distance_data['distance']}"
    
    # Light data
    if light_data and 'cahaya cuaca' in light_data:
        light_info = light_data['cahaya cuaca']  # e.g., "Mendung(20.83 lux)"
        light_value = light_info.split("(")[1].replace(" lux)", "")  # Extract the lux value
        light_condition = light_info.split("(")[0]  # Extract the condition description
        light_abbreviation = light_weather_map.get(light_condition, "N/A")  # Get abbreviation for light condition
    else:
        # If no light data or lux is 0, assume it's "Malam/Hujan"
        light_value = "0"
        light_abbreviation = "(M/H)"

    light_description = f"L:{light_value},{light_abbreviation}"

    # Concatenate all the data
    return f"R:{rain}|W:{wind}|D:{distance}|{light_description}"

# Main function to handle sensor data collection and communication
if __name__ == "__main__":
    try:
        # Start all sensors in separate threads
        threading.Thread(target=run_rain_gauge, daemon=True).start()
        threading.Thread(target=run_anonemeter, daemon=True).start()
        threading.Thread(target=run_bh1750, daemon=True).start()
        threading.Thread(target=run_ultrasonic, daemon=True).start()

        # Start Zigbee receiver in a separate thread
        threading.Thread(target=receive_message, daemon=True).start()


        # Main loop to collect sensor data and send messages
        while True:
            # Get data from all sensors
            rain_data = get_rainfall_data()
            wind_data = get_wind_data()
            distance_data = get_distance_data()
            light_data = get_light_data()

            # Format the data to reduce size
            current_data = format_data(rain_data, wind_data, distance_data, light_data)

            # Get the current time in seconds since the epoch
            current_time = time.strftime("%H:%M:%S", time.localtime())

            # Print the current time and data
            print(f"Current time: {current_time}")
            print(f"Formatted data: {current_data}")

            # Send data via Zigbee
            send_message_to_remote(current_data, current_time)

            time.sleep(10)  # Adjust sleep time as needed

    except KeyboardInterrupt:
        print('System stopped by user.')
    finally:
        with device_lock:
            if device.is_open():
                device.close()
        print('Cleaning up resources.')
