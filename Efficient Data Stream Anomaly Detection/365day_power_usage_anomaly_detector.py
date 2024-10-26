import numpy as np
import random
import matplotlib.pyplot as plt

# Z-Score based anomaly detection using a rolling mean and standard deviation
def is_anomaly(data, window=30, threshold=2):
    if len(data) < window:
        return False  # Not enough data for anomaly detection yet
    rolling_mean = np.mean(data)
    rolling_std = np.std(data)
    z_score = (data[-1] - rolling_mean) / rolling_std
    return abs(z_score) > threshold

# Simulate voltage generation over 365 days
def simulate_voltage_stream(days=365, normal_voltage=230, fluctuation=5, anomaly_chance=0.05, anomaly_magnitude=50):
    for day in range(days):
        # Simulate normal voltage with small fluctuations
        voltage = normal_voltage + random.uniform(-fluctuation, fluctuation)

        # Randomly introduce an anomaly (voltage spike or drop)
        if random.random() < anomaly_chance:
            voltage += random.uniform(anomaly_magnitude * -1, anomaly_magnitude)

        yield voltage

# Scatter plot with anomaly detection
def scatter_plot_voltages(voltage_stream, window=30, threshold=2):
    voltages = []
    anomalies_x = []
    anomalies_y = []
    total_anomalies = 0
    
    for day, voltage in enumerate(voltage_stream):
        voltages.append(voltage)
        
        if is_anomaly(voltages[-window:], window, threshold):
            anomalies_x.append(day)
            anomalies_y.append(voltage)
            total_anomalies += 1

    # Create scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(range(len(voltages)), voltages, color='blue', label='Voltage')
    plt.scatter(anomalies_x, anomalies_y, color='red', label='Anomalies')
    
    plt.title("Voltage Readings of Generator Over 365 Days")
    plt.xlabel("Day")
    plt.ylabel("Voltage (V)")
    plt.legend()
    plt.grid(True)
    plt.show()

    print(f"Total number of anomalies detected: {total_anomalies}")

# Main execution
if __name__ == "__main__":
    voltage_stream = simulate_voltage_stream(days=365)
    scatter_plot_voltages(voltage_stream)


