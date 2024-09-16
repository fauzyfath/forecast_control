import smbus
import time
from bh1750 import BH1750

# Membuat bus I2C
bus = smbus.SMBus(1)  # Pada Raspberry Pi, biasanya menggunakan I2C-1

# Inisialisasi sensor BH1750
sensor = BH1750(bus)

try:
    # Mengatur mode ke CONTINUOUS_HIGH_RES_MODE dengan alamat 0x23
    sensor.power_on()
    sensor.reset()
    
    print("BH1750 Light Sensor initialized")

    while True:
        # Membaca tingkat pencahayaan
        lux = sensor.lux()

        # Cek apakah pembacaan berhasil
        if lux > 50:
            print(f"Cerah: {lux:.2f} lux")
        elif lux < 50:
            print(f"Mendung: {lux:.2f} lux")
        else:
            print("Error reading light level")
        
        time.sleep(1)

except Exception as e:
    print(f"Error initializing or reading BH1750: {e}")

finally:
    # Mematikan sensor untuk menghemat daya
    sensor.power_off()
