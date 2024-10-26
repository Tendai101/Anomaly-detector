import numpy as np
import random
import matplotlib.pyplot as plt
from collections import deque
import time

# Anomaly detection using both Z-score and fixed threshold
def is_anomaly(data, threshold=2, fixed_threshold=10):
    if len(data) == 0:
        return False  # Not enough data for anomaly detection yet
    rolling_mean = np.mean(data)
    rolling_std = np.std(data)
    z_score = (data[-1] - rolling_mean) / rolling_std
    
    # Check for anomalies using both z-score and a fixed voltage threshold
    return abs(z_score) > threshold or abs(data[-1] - rolling_mean) > fixed_threshold

# Simulate real-time voltage readings (1 per second)
def simulate_voltage_stream(duration=30, normal_voltage=230, fluctuation=5, anomaly_chance=0.1, anomaly_magnitude=50):
    for _ in range(duration):
        # Simulate normal voltage with small fluctuations
        voltage = normal_voltage + random.uniform(-fluctuation, fluctuation)

        # Randomly introduce an anomaly (voltage spike or drop)
        if random.random() < anomaly_chance:
            voltage += random.uniform(anomaly_magnitude * -1, anomaly_magnitude)

        yield voltage

# Real-time line graph with anomaly detection
def real_time_line_plot_with_anomalies(duration=30, window=10, threshold=2):
    plt.ion()  # Turn on interactive mode for real-time plotting
    fig, ax = plt.subplots()
    ax.set_ylim(150, 300)  # Set voltage limits (assuming voltage ranges)
    
    voltages = []  # Store all voltage readings
    times = []  # Store the time points for the x-axis
    anomalies_x, anomalies_y = [], []
    total_anomalies = 0
    anomaly_count = 1  # For labeling the anomalies

    # Setup the plot title and labels
    plt.title("Real-Time Voltage Monitoring with Anomalies")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Voltage (V)")

    # Initial plot
    voltage_line, = ax.plot([], [], color='blue', label='Voltage')
    anomaly_scatter = ax.scatter([], [], color='red', s=50, zorder=5, label='Anomalies')

    # Add legend only once
    ax.legend()

    for i, voltage in enumerate(simulate_voltage_stream(duration)):
        times.append(i)
        voltages.append(voltage)

        # Detect anomalies using a rolling window
        if len(voltages) >= window:  # Only check for anomalies if we have enough data
            if is_anomaly(voltages[-window:], threshold):
                anomalies_x.append(i)
                anomalies_y.append(voltage)
                total_anomalies += 1
                ax.annotate(f"Anomaly {anomaly_count}",  # Annotate each anomaly
                            xy=(i, voltage),
                            xytext=(i, voltage + 10),
                            arrowprops=dict(facecolor='red', shrink=0.05),
                            fontsize=8,
                            color='red')
                anomaly_count += 1

        # Update the line and scatter data
        voltage_line.set_data(times, voltages)
        anomaly_scatter.set_offsets(np.c_[anomalies_x, anomalies_y])

        # Update labels and limits dynamically
        ax.set_xlim(0, max(1, i + 1))  # Set x-axis limits based on the current time
        ax.set_ylim(150, 300)

        # Redraw the plot with updated data
        plt.draw()
        plt.pause(0.01)  # Pause to simulate real-time updates

        # Simulate real-time by waiting 1 second per reading
        time.sleep(1)

    plt.ioff()  # Turn off interactive mode
    plt.show()

    print(f"Total number of anomalies detected: {total_anomalies}")

# Main execution
if __name__ == "__main__":
    # 30 seconds duration for the real-time voltage monitoring
    real_time_line_plot_with_anomalies(duration=30)  # Simulate voltage for 30 seconds (one reading per second)



