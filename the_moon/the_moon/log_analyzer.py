import os
import argparse

def calculate_log_averages(file_path, trim_percent):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    valid_lines_data = []
    ignored_low_snr_count = 0

    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, 1):
            parts = line.strip().split()
            
            # Skip empty lines or Ping ('P') lines
            if not parts or parts[0] != 'S':
                continue
                
            # Ensure the line has the correct number of elements
            if len(parts) != 11:
                print(f"Warning: Skipping malformed line {line_num}: {line.strip()}")
                continue
                
            try:
                snr_value = float(parts[2])
                rem_snr_value = float(parts[3])
                
                # Ignore rows where local SNR or remote SNR is <= 0
                if snr_value <= 0 or rem_snr_value <= 0:
                    ignored_low_snr_count += 1
                    continue

                row_data = {
                    'SNR':      snr_value,
                    'rem_SNR':  rem_snr_value,
                    'rssi':     float(parts[4]),
                    'remrssi':  float(parts[5]),
                    'txbuf':    float(parts[6]),
                    'noise':    float(parts[7]),
                    'remnoise': float(parts[8]),
                    'rxerrors': float(parts[9]),
                    'fixed':    float(parts[10])
                }
                valid_lines_data.append(row_data)
                
            except ValueError:
                print(f"Warning: Non-numeric data found on line {line_num}: {line.strip()}")
                continue

    total_valid_lines = len(valid_lines_data)
    print(f"\n--- Log File Parsed: {file_path} ---")
    print(f"Ignored lines due to SNR or rem_SNR <= 0: {ignored_low_snr_count}")
    print(f"Total valid 'S' lines kept: {total_valid_lines}")
    
    if total_valid_lines == 0:
        print("No valid status lines left to average after applying filters.")
        return

    # Calculate how many lines to trim based on the remaining valid lines
    trim_amount = int(total_valid_lines * (trim_percent / 100.0))
    
    if trim_amount > 0:
        trimmed_data = valid_lines_data[trim_amount : total_valid_lines - trim_amount]
        print(f"Trimmed {trim_percent}% ({trim_amount} lines) from the start and the end.")
    else:
        trimmed_data = valid_lines_data
        print(f"Not enough lines to trim {trim_percent}%. Using all valid lines.")

    processed_count = len(trimmed_data)
    print(f"Total messages (lines) analyzed: {processed_count}\n")

    if processed_count == 0:
        print("No lines left to process after trimming.")
        return

    metrics_sums = {
        'SNR': 0.0, 'rem_SNR': 0.0, 'rssi': 0.0, 'remrssi': 0.0,
        'txbuf': 0.0, 'noise': 0.0, 'remnoise': 0.0, 'rxerrors': 0.0, 'fixed': 0.0
    }

    for row in trimmed_data:
        for metric in metrics_sums:
            metrics_sums[metric] += row[metric]

    print(f"{'Metric':<12} | {'Value':<15}")
    print("-" * 30)
    
    for metric, total_sum in metrics_sums.items():
        if metric in ['rxerrors', 'fixed']:
            print(f"{metric:<12} | {int(total_sum):<10} (Total)")
        else:
            average = total_sum / processed_count
            print(f"{metric:<12} | {average:<10.2f} (Average)")

    print("-" * 30)
    total_errors = int(metrics_sums['rxerrors'])
    print(f"SUMMARY: {total_errors} errors out of {processed_count} analyzed messages.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Calculate averages and error totals from radio log files.")
    
    parser.add_argument(
        "file_path", 
        help="Path to the log file to be parsed"
    )
    
    parser.add_argument(
        "-t", "--trim", 
        type=int, 
        default=10, 
        help="Percentage of data to trim from both ends (default: 10)"
    )
    
    args = parser.parse_args()
    calculate_log_averages(args.file_path, args.trim)