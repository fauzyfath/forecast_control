import RPi.GPIO as GPIO
import time
from datetime import datetime

# Constants
GPIO_PULSE = 18  # GPIO pin number (BCM numbering)
UPDATE_INTERVAL = 10  # Seconds

# Variables
rpmcount = 0
last_micros = time.time() * 1_000_000
timeold = time.time()
rotasi_per_detik = 0.0
kecepatan_meter_per_detik = 0.0
kecepatan_kilometer_per_jam = 0.0

def rpm_anemometer(channel): 
    global rpmcount, last_micros
    current_micros = time.time() * 1_000_000
    if (current_micros - last_micros) >= 5000:  # 5 milliseconds
        rpmcount += 1
        last_micros = current_micros

def get_system_time():
    now = datetime.now()
    return now.hour, now.minute, now.second

def get_wind_data():
    return {
        "rotasi_per_detik": rotasi_per_detik,
        "kecepatan_meter_per_detik": kecepatan_meter_per_detik,
        "kecepatan_kilometer_per_jam": kecepatan_kilometer_per_jam
    }

def print_serial(hours, minutes, seconds):
    jam = str(hours).zfill(2)
    menit = str(minutes).zfill(2)
    detik = str(seconds).zfill(2)

    # print(f"{jam}:{menit}:{detik}")
    # print(f"Kecepatan angin={kecepatan_meter_per_detik:.2f} m/s")
    # print(f"Kecepatan angin={kecepatan_kilometer_per_jam:.2f} km/h")

def run_anonemeter():
    global GPIO_PULSE
    global rpmcount
    global last_micros
    global timeold
    global rotasi_per_detik
    global kecepatan_meter_per_detik
    global kecepatan_kilometer_per_jam

    # Setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PULSE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(GPIO_PULSE, GPIO.RISING, callback=rpm_anemometer)

    try:
        last_update = time.time()
        while True:
            current_time = time.time()
            elapsed_time = current_time - last_update

            if elapsed_time >= UPDATE_INTERVAL:
                rotasi_per_detik = float(rpmcount) / UPDATE_INTERVAL
                kecepatan_meter_per_detik = (-0.0181 * (rotasi_per_detik ** 2) + 1.3859 * rotasi_per_detik + 1.4055)
                
                # Filter out speeds below threshold
                if kecepatan_meter_per_detik <= 1.5:
                    kecepatan_meter_per_detik = 0.0

                kecepatan_kilometer_per_jam = kecepatan_meter_per_detik * 3.6

                hours, minutes, seconds = get_system_time()

                # Print data
                print_serial(hours, minutes, seconds)

                # Reset counters
                rpmcount = 0
                last_update = current_time

            time.sleep(1)  # Sleep to prevent high CPU usage

    except KeyboardInterrupt:
        print("Program stopped by user")
    
    finally:
        GPIO.cleanup()
