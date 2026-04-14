import sys
import os
import matplotlib.pyplot as plt

def calculate_running_average(data, window_size):
    """Calculates the running average of a list, handling the start of the list gracefully."""
    smoothed = []
    for i in range(len(data)):
        # Get the window of previous data points up to the current point
        start_idx = max(0, i - window_size + 1)
        window = data[start_idx:i+1]
        smoothed.append(sum(window) / len(window))
    return smoothed

def plot_status_logs(file_path, window_size=10):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    # Data lists
    times = []
    snr, rem_snr = [], []
    rssi, remrssi = [], []
    noise, remnoise = [], []

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            
            # Filter for 'S' lines and check length
            if not parts or parts[0] != 'S' or len(parts) != 11:
                continue
            
            try:
                # Log format: S {time_usec} {SNR} {rem_SNR} {rssi} {remrssi} {txbuf} {noise} {remnoise} {rxerrors} {fixed}
                times.append(int(parts[1]))
                snr.append(float(parts[2]))
                rem_snr.append(float(parts[3]))
                rssi.append(float(parts[4]))
                remrssi.append(float(parts[5]))
                noise.append(float(parts[7]))
                remnoise.append(float(parts[8]))
            except ValueError:
                continue
    
    if not times:
        print("No valid status ('S') data found to plot.")
        return

    # Normalize timestamps to relative seconds (starting at t=0)
    start_time = times[0]
    times_sec = [(t - start_time) / 1_000_000.0 for t in times]

    # Calculate Running Averages
    snr_avg = calculate_running_average(snr, window_size)
    rem_snr_avg = calculate_running_average(rem_snr, window_size)
    rssi_avg = calculate_running_average(rssi, window_size)
    remrssi_avg = calculate_running_average(remrssi, window_size)
    noise_avg = calculate_running_average(noise, window_size)
    remnoise_avg = calculate_running_average(remnoise, window_size)

    # Create figure and 3 subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    
    # --- 1. SNR Plot ---
    # Plot raw data (faded)
    ax1.plot(times_sec, snr, color='blue', alpha=0.2, label='_nolegend_')
    ax1.plot(times_sec, rem_snr, color='orange', alpha=0.2, label='_nolegend_')
    # Plot running average (solid)
    ax1.plot(times_sec, snr_avg, label=f'Local SNR (Avg {window_size})', color='blue', linewidth=2)
    ax1.plot(times_sec, rem_snr_avg, label=f'Remote SNR (Avg {window_size})', color='orange', linewidth=2)
    ax1.set_ylabel('SNR')
    ax1.set_title(f'Radio Status Over Time (Window: {window_size})\n{os.path.basename(file_path)}')
    ax1.legend(loc='upper right')
    ax1.grid(True, linestyle='--', alpha=0.7)

    # --- 2. RSSI Plot ---
    ax2.plot(times_sec, rssi, color='green', alpha=0.2, label='_nolegend_')
    ax2.plot(times_sec, remrssi, color='red', alpha=0.2, label='_nolegend_')
    ax2.plot(times_sec, rssi_avg, label=f'Local RSSI (Avg {window_size})', color='green', linewidth=2)
    ax2.plot(times_sec, remrssi_avg, label=f'Remote RSSI (Avg {window_size})', color='red', linewidth=2)
    ax2.set_ylabel('RSSI')
    ax2.legend(loc='upper right')
    ax2.grid(True, linestyle='--', alpha=0.7)

    # --- 3. Noise Plot ---
    ax3.plot(times_sec, noise, color='purple', alpha=0.2, label='_nolegend_')
    ax3.plot(times_sec, remnoise, color='brown', alpha=0.2, label='_nolegend_')
    ax3.plot(times_sec, noise_avg, label=f'Local Noise (Avg {window_size})', color='purple', linewidth=2)
    ax3.plot(times_sec, remnoise_avg, label=f'Remote Noise (Avg {window_size})', color='brown', linewidth=2)
    ax3.set_ylabel('Noise')
    ax3.set_xlabel('Time (seconds)')
    ax3.legend(loc='upper right')
    ax3.grid(True, linestyle='--', alpha=0.7)

    # Adjust layout so labels don't overlap
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # You can configure the smoothing window here (default is 10 points)
    SMOOTHING_WINDOW = 25

    # Pass the log file as a command-line argument
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
    else:
        log_file = '/home/meciek/the_moon/test_static_3/radio433_log_msgs_received_GS_1776109078.txt' 
        print(f"No file provided. Attempting to read default: {log_file}")
        
    plot_status_logs(log_file, window_size=SMOOTHING_WINDOW)