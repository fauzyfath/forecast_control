# rainGauge.py
import RPi.GPIO as GPIO
import time
from datetime import datetime

# Constants
PIN_INTERRUPT = 16  # GPIO pin number (BCM numbering)
MILLIMETER_PER_TIP = 0.70
UPDATE_INTERVAL = 10  # Seconds

# Variables
jumlah_tip = 0
curah_hujan = 0.00
curah_hujan_per_menit = 0.00
curah_hujan_per_jam = 0.00
curah_hujan_per_hari = 0.00
curah_hujan_hari_ini = 0.00
temp_curah_hujan_per_menit = 0.00
temp_curah_hujan_per_jam = 0.00
temp_curah_hujan_per_hari = 0.00
temp_jumlah_tip = 0

cuaca = "Berawan"
flag = False

def hitung_curah_hujan(channel):
    global flag
    flag = True
    print("Interrupt detected!")  # Debugging line

def get_system_time():
    now = datetime.now()
    return now.hour, now.minute, now.second

def get_rainfall_data():
    return {
        "jumlah_tip": jumlah_tip,
        "curah_hujan_per_menit": curah_hujan_per_menit,
        "curah_hujan_per_jam": curah_hujan_per_jam,
        "curah_hujan_per_hari": curah_hujan_per_hari,
        "curah_hujan_hari_ini": curah_hujan_hari_ini,
        "cuaca": cuaca
    }

def print_serial(hours, minutes, seconds):
    jam = str(hours).zfill(2)
    menit = str(minutes).zfill(2)
    detik = str(seconds).zfill(2)

    # print(f"{jam}:{menit}:{detik}")
    # print(f"Cuaca={cuaca}")
    # print(f"Jumlah tip={jumlah_tip} kali")
    # print(f"Curah hujan hari ini={curah_hujan_hari_ini:.1f} mm")
    # print(f"Curah hujan per menit={curah_hujan_per_menit:.1f} mm")
    # print(f"Curah hujan per jam={curah_hujan_per_jam:.1f} mm")
    # print(f"Curah hujan per hari={curah_hujan_per_hari:.1f} mm")

def run_rain_gauge():
    global last_update
    global curah_hujan
    global curah_hujan_per_menit
    global curah_hujan_per_jam
    global curah_hujan_per_hari
    global curah_hujan_hari_ini
    global jumlah_tip
    global temp_curah_hujan_per_menit
    global temp_curah_hujan_per_jam
    global temp_curah_hujan_per_hari
    global temp_jumlah_tip
    global cuaca
    global flag
    
    # Setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_INTERRUPT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(PIN_INTERRUPT, GPIO.FALLING, callback=hitung_curah_hujan, bouncetime=200)
    
    try:
        last_update = time.time()
        while True:
            current_time = time.time()
            elapsed_time = current_time - last_update
            
            if flag:
                curah_hujan += MILLIMETER_PER_TIP
                jumlah_tip += 1
                flag = False
                # print(f"Tip detected! Total tips: {jumlah_tip}")  # Debugging line
            
            hours, minutes, seconds = get_system_time()
            
            curah_hujan_hari_ini = jumlah_tip * MILLIMETER_PER_TIP
            
            # Update weather condition based on rainfall amount
            if curah_hujan_hari_ini <= 0.00:
                cuaca = "Berawan"
            elif curah_hujan_hari_ini <= 0.50:
                cuaca = "Berawan"
            elif curah_hujan_hari_ini <= 20.00:
                cuaca = "Hujan Ringan"
            elif curah_hujan_hari_ini <= 50.00:
                cuaca = "Hujan Sedang"
            elif curah_hujan_hari_ini <= 100.00:
                cuaca = "Hujan Lebat"
            elif curah_hujan_hari_ini <= 150.00:
                cuaca = "Hujan Sangat Lebat"
            else:
                cuaca = "Hujan ekstrem"
            
            if elapsed_time >= UPDATE_INTERVAL:  # Check if the update interval has passed
                # Reset for new interval
                temp_curah_hujan_per_menit = curah_hujan
                curah_hujan_per_menit = temp_curah_hujan_per_menit
                
                temp_curah_hujan_per_jam += curah_hujan_per_menit
                curah_hujan_per_jam = temp_curah_hujan_per_jam
                
                if minutes == 0:
                    curah_hujan_per_hari += curah_hujan_per_jam
                    temp_curah_hujan_per_jam = 0.00
                
                if minutes == 0 and hours == 0:
                    curah_hujan_per_hari = temp_curah_hujan_per_hari
                    temp_curah_hujan_per_hari = 0.00
                    curah_hujan_hari_ini = 0.00
                    jumlah_tip = 0
                
                # Reset current period variables
                curah_hujan = 0.00
                
                # Update the last update time
                last_update = current_time
                
                if jumlah_tip != temp_jumlah_tip or seconds == 0:
                    print_serial(hours, minutes, seconds)
                
                temp_jumlah_tip = jumlah_tip
            
            time.sleep(1)  # Sleep for a short period to prevent high CPU usage

    except KeyboardInterrupt:
        print("Program stopped by user")
    
    finally:
        GPIO.cleanup()
