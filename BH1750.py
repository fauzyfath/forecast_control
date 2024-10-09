import smbus
import time

# I2C address of the BH1750
BH1750_ADDRESS = 0x23  # Default I2C address
POWER_ON = 0x01
RESET = 0x07
CONTINUOUS_HIGH_RES_MODE = 0x10

# Global variable to store light data
current_light_data = None

def initialize_sensor(bus):
    bus.write_byte(BH1750_ADDRESS, POWER_ON)
    time.sleep(0.1)
    bus.write_byte(BH1750_ADDRESS, RESET)
    time.sleep(0.1)
    bus.write_byte(BH1750_ADDRESS, CONTINUOUS_HIGH_RES_MODE)

def read_light(bus):
    data = bus.read_i2c_block_data(BH1750_ADDRESS, CONTINUOUS_HIGH_RES_MODE, 2)
    light = (data[0] << 8) | data[1]
    return light / 1.2

def get_light_data():
    global current_light_data
    return current_light_data

def run_bh1750():
    global current_light_data
    bus = smbus.SMBus(1)
    initialize_sensor(bus)
    try:
        while True:
            lux = read_light(bus)
            if lux > 10 and lux < 50:
                lux_output = f"Mendung({lux:.2f} lux)"
            elif lux > 50:
                lux_output = f"Cerah({lux:.2f} lux)"
            elif lux <= 10:
                lux_output = f"Malam/Hujan({lux:.2f} lux)"
            else:
                lux_output = "Error reading light level"

            # Store the light data globally
            current_light_data = {
                "cahaya cuaca": lux_output
            }

            time.sleep(1)
    except Exception as e:
        print(f"Error initializing or reading BH1750: {e}")
    finally:
        bus.write_byte(BH1750_ADDRESS, 0x00)  # Power off the sensor
