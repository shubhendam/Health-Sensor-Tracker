import threading
import time
from motion_classifier import classify_motion
from get_sensor_data import accel_data, gyro_data  # Assuming these are global variables in get_sensor_data.py

# Global variable to store the current activity
current_activity = None

def activity_tracking_loop():
    global current_activity
    while True:
        # Classify motion every 2 seconds
        current_activity = classify_motion(accel_data, gyro_data)
        time.sleep(2)

def start_activity_tracking(user):
    global current_activity
    current_activity = "Static"  # Initialize with a default activity
    # Start the activity tracking loop in a separate thread
    threading.Thread(target=activity_tracking_loop, daemon=True).start()

def get_current_activity():
    global current_activity
    return current_activity