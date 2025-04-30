# Health-Sensor-Tracker

## 1. Activity Tracker – GenAI-Powered Wellness Assistant

Activity Tracker is a real-time, privacy-respecting health and activity companion powered by Generative AI and sensor data.

This desktop application connects to your smartphone sensors to track your physical activity (walking, running, climbing stairs, sitting/static), evaluates your movements based on your health profile and local weather, and delivers personalized, motivational advice through an on-device LLM.

The system blends motion detection, user profiling, environmental awareness, and GenAI reasoning to act like a virtual coach — encouraging, supportive, and smart.

> Built with a focus on privacy, edge intelligence, and modular architecture. Designed for the future of human-centered AI.



## 2. Setup

To run this app locally on your system, follow these steps:

### Clone and Setup Virtual Environment

#### Windows
```bash
git clone https://github.com/shubhendam/Health-Sensor-Tracker.git
cd Health-Sensor-Tracker
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux
```bash
git clone https://github.com/shubhendam/Health-Sensor-Tracker.git
cd Health-Sensor-Tracker
python3 -m venv venv
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

### Download LLM & Embedding Models

- [LLaMA 3.2 3B (GGUF)](https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q4_K_M.gguf?download=true)  


Place `.gguf` files in the `models/` directory.

### Download Application on your Phone 

- Download Sensor Server App(Android)(https://f-droid.org/F-Droid.apk)

Click "Start" on screen and copy the URL for websocket and put the url in get_sensor_data.py
```python
# Thread for Accelerometer
threading.Thread(target=connect, args=("ws://<URL from app>/sensor/connect?type=android.sensor.accelerometer", on_message_accel)).start()

# Thread for Gyroscope
threading.Thread(target=connect, args=("ws://<URL from app>/sensor/connect?type=android.sensor.gyroscope", on_message_gyro)).start()

# Thread for Gravity
threading.Thread(target=connect, args=("ws://<URL from app>/sensor/connect?type=android.sensor.gravity", on_message_gravity)).start()
   ```

## 3. Running the APP

Run the app with:

```bash
streamlit run main.py
```
### In the UI: 

1. Click on "Start" in App before running the app
2. Select Either: **Login** or **Sign Up**
3. When Login, Give current location


### Sample Screen Shot:
![Screenshot](asset/Screenshot (25).png)

## 4. Future Enhancements
1. Calibrate sensor data to extract better accuracy to calculate Steps

