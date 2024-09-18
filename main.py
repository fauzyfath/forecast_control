# main.py
import time
import threading
from rainGauge import run_rain_gauge, get_rainfall_data
from anonemeter import run_anonemeter, get_wind_data
# from ultrasonic import run_ultrasonic, get_distance_data
from BH1750 import run_bh1750, get_light_data

def show_data_collection():
    # Fetch and display the latest rainfall data
    # rainData = get_rainfall_data()
    # print("Current Rainfall Data:")
    # print(rainData)

    # # Fetch and display the latest wind data
    # windData = get_wind_data()
    # print("Current wind Data:")
    # print(windData)

    # # Fetch and display the latest distance data
    # distanceData = get_distance_data()
    # print("Current distance Data:")
    # print(distanceData)

    lightData = get_light_data()
    print("current light Data:")
    print(lightData)
    
def run_rain_gauge_thread():
    # Run the rain gauge in a separate thread
    run_rain_gauge()

def run_anonemeter_thread():
    # Run the anonemeter in seperate thread
    run_anonemeter()

# def run_ultrasonic_thread():
#     # Run the ultrasonic in seperate thread 
#     run_ultrasonic()

def run_bh1750_thread():
    run_bh1750()

if __name__ == "__main__":
    try:
        # Start the rain gauge in a separate thread
        # gauge_thread = threading.Thread(target=run_rain_gauge_thread, daemon=True)
        # gauge_thread.start()
        # anonemeter_thread = threading.Thread(target=run_anonemeter_thread, daemon=True)
        # anonemeter_thread.start()
        bh1750_thread = threading.Thread(target=run_bh1750_thread, daemon=True)
        bh1750_thread.start()

        while True:
            # Fetch rainfall data
            rainfall_data = get_rainfall_data()
            # Fetch wind data
            wind_data = get_wind_data()
            # fetch distance data (distance max 1 meter)
            # distance_data = get_distance_data()
            
            # Optionally display the data to the console
            show_data_collection()
            
            time.sleep(10)  # Adjust sleep time as needed

    except KeyboardInterrupt:
        print('System stopped by user.')
    finally:
        print('Cleaning up resources.')
