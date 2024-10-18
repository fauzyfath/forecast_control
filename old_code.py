# main.py
import time
import threading
import serial 
from rainGauge import run_rain_gauge, get_rainfall_data
from anonemeter import run_anonemeter, get_wind_data
from ultrasonic import run_ultrasonic, get_distance_data
from BH1750 import run_bh1750, get_light_data
from camera import capture_image

# Konfigurasi port serial dan kecepatan baudrate
PORT = '/dev/tty7'  # Ganti dengan port yang sesuai
BAUD_RATE = 9600

def send_message(data):
    with serial.Serial(PORT, BAUD_RATE, timeout=1) as ser:
        time.sleep(2)  # Tunggu sampai port terbuka
        ser.write(data.encode())
        print(f"Data dikirim: {data}")

def run_zigbee_receiver(port='/dev/tty7', baud_rate=9600):
    # Receive messages from the Zigbee module and trigger camera capture on 'activate'.
    with serial.Serial(port, baud_rate, timeout=1) as ser:
        print("Zigbee receiver started. Waiting for messages...")
        while True:
            if ser.in_waiting > 0:
                # Read the incoming message
                message = ser.readline().decode('utf-8').strip()
                print(f"Received message: {message}")
                
                # Check if the action is "activate"
                if message.lower() == "activate":
                    capture_image('/images')  # Adjust the directory as needed

def run_rain_gauge_thread():
    # Run the rain gauge in a separate thread
    run_rain_gauge()

def run_anonemeter_thread():
    # Run the anonemeter in seperate thread
    run_anonemeter()

def run_ultrasonic_thread():
    # Run the ultrasonic in seperate thread 
    run_ultrasonic()

def run_bh1750_thread():
    # Run the lightsensor in seperate thread
    run_bh1750()

if __name__ == "__main__":
    try:
        # Start the all sensors in a separate thread
        gauge_thread = threading.Thread(target=run_rain_gauge_thread, daemon=True)
        gauge_thread.start()
        anonemeter_thread = threading.Thread(target=run_anonemeter_thread, daemon=True)
        anonemeter_thread.start()
        bh1750_thread = threading.Thread(target=run_bh1750_thread, daemon=True)
        bh1750_thread.start()
        ultrasonic_thread = threading.Thread(target=run_ultrasonic_thread, daemon=True)
        ultrasonic_thread.start()

        while True:
            # all sensor data 
            rainData = get_rainfall_data()
            windData = get_wind_data()
            distanceData = get_distance_data()
            lightData = get_light_data()

            # Combine all data into one variable (string)
            current_data = f"Rainfall:{rainData}, Wind:{windData}, Distance:{distanceData}, Light:{lightData}"

            # Get the current time in seconds since the epoch
            current_time = time.time()
            
            # Convert it to a readable format
            local_time = time.localtime(current_time)
            formatted_time = time.strftime("%H:%M:%S", local_time)
            
            # Print the current time
            print("Current time:", formatted_time)
            print(current_data)
            
            # send_message(current_data)

            time.sleep(10)  # Adjust sleep time as needed

    except KeyboardInterrupt:
        print('System stopped by user.')
    finally:\
        print('Cleaning up resources.')
