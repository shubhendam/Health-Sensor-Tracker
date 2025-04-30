import websocket
import threading
import json
import numpy as np
import time
from motion_classifier import classify_motion  # Import the classifier function

# --- Global Variables ---
STEP_THRESHOLD = 2.0
MIN_TIME_BETWEEN_STEPS = 0.4
last_step_time = 0
step_count = 0

gravity = np.array([0.0, 0.0, 0.0])
accel_data = []  # Store accelerometer data for classification
gyro_data = []   # Store gyroscope data for classification
last_print_time = 0  # Track the last time motion was printed

# --- Functions ---

def detect_step(linear_x, linear_y, linear_z, current_time):
    global last_step_time, step_count
    magnitude = np.sqrt(linear_x**2 + linear_y**2 + linear_z**2)

    if magnitude > STEP_THRESHOLD:
        if (current_time - last_step_time) > MIN_TIME_BETWEEN_STEPS:
            step_count += 1
            last_step_time = current_time
            print(f"[STEP DETECTED] Total steps: {step_count}")

def get_current_steps():
    global step_count
    return step_count

def on_message_accel(ws, message):
    global gravity, accel_data, last_print_time
    values = json.loads(message)['values']
    x, y, z = values
    current_time = time.time()

    # Subtract gravity to get pure motion
    linear_acc = np.array([x, y, z]) - gravity

    detect_step(linear_acc[0], linear_acc[1], linear_acc[2], current_time)

    # Store accelerometer data for classification
    accel_data.append(linear_acc)
    if len(accel_data) > 100:  # Keep only the last 100 samples
        accel_data.pop(0)

    #print(f"[ACCEL] x = {x:.3f}, y = {y:.3f}, z = {z:.3f}")

    # Classify motion every 2 seconds
    if (current_time - last_print_time) >= 2:
        motion = classify_motion(accel_data, gyro_data)
        print(f"[MOTION] {motion}")
        last_print_time = current_time

def on_message_gyro(ws, message):
    global gyro_data
    values = json.loads(message)['values']
    gx, gy, gz = values

    # Store gyroscope data for classification
    gyro_data.append(np.array([gx, gy, gz]))
    if len(gyro_data) > 100:  # Keep only the last 100 samples
        gyro_data.pop(0)

    #print(f"[GYRO] gx = {gx:.3f}, gy = {gy:.3f}, gz = {gz:.3f}")

def on_message_gravity(ws, message):
    global gravity
    values = json.loads(message)['values']
    gravity = np.array(values)
    #print(f"[GRAVITY] gx = {gravity[0]:.3f}, gy = {gravity[1]:.3f}, gz = {gravity[2]:.3f}")

def connect(url, on_message_func):
    ws = websocket.WebSocketApp(url,
                                 on_open=lambda ws: print(f"Connected to {url}"),
                                 on_message=on_message_func,
                                 on_error=lambda ws, err: print(f"Error: {err}"),
                                 on_close=lambda ws, code, reason: print(f"Closed: {reason}"))
    ws.run_forever()

# --- Start Streaming Threads ---

# Thread for Accelerometer
threading.Thread(target=connect, args=("ws://192.168.0.108:8080/sensor/connect?type=android.sensor.accelerometer", on_message_accel)).start()

# Thread for Gyroscope
threading.Thread(target=connect, args=("ws://192.168.0.108:8080/sensor/connect?type=android.sensor.gyroscope", on_message_gyro)).start()

# Thread for Gravity
threading.Thread(target=connect, args=("ws://192.168.0.108:8080/sensor/connect?type=android.sensor.gravity", on_message_gravity)).start()
