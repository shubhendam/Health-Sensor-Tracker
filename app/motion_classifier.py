import numpy as np

def calculate_features(data):
    if len(data) == 0:
        return np.zeros(3)
    data = np.array(data)
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)
    magnitude = np.linalg.norm(data, axis=1)
    max_magnitude = np.max(magnitude)
    return np.concatenate([mean, std, [max_magnitude]])

def classify_motion(accel_data, gyro_data):
    accel_features = calculate_features(accel_data)
    gyro_features = calculate_features(gyro_data)

    features = np.concatenate([accel_features, gyro_features])

    # Define thresholds for classification
    if features[5] < 0.5:  # Low standard deviation in accelerometer data
        return "Static"
    elif features[5] < 2.0 and features[8] < 1.0:  # Moderate acceleration and low gyroscope activity
        return "Walking"
    else:
        return "Running"
