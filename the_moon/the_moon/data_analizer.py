# import matplotlib for plots
import matplotlib.pyplot as plt
import os

def main():
    file_rocket_msgs_received = "the_moon/radio433_log_msgs_received_rocket_1770919391.txt"
    file_GS_msgs_received = "the_moon/radio433_log_msgs_received_GS_1770919391.txt"

    file_rocket_pings_sent = "the_moon/radio433_log_pings_sent_rocket_1770919391.txt"
    file_GS_pings_sent = "the_moon/radio433_log_pings_sent_GS_1770919391.txt"

    # create folder "plots" if does not exist
    if not os.path.exists("plots"):
        os.makedirs("plots")

    # =================== analize radio status ===================

    with open(file_rocket_msgs_received, 'r') as f:
        # vector of timestamps, vector of SNR, vector of rem_SNR
        time_usec = []
        SNR = []
        rem_SNR = []
        # vector of RSSI, rem_RSSI, Noise, rem_Noise
        rssi = []
        rem_rssi = []
        noise = []
        rem_noise = []
        # vectors for txbuf, rxerrors and fixed
        txbuf = []
        rxerrors = []
        fixed = []
        for line in f:
            # devide by space
            parts = line.split(' ')
            if parts[0] == 'S':
                time_usec.append(int(parts[1]))
                SNR.append(int(parts[2]))
                rem_SNR.append(int(parts[3]))
                rssi.append(int(parts[4]))
                rem_rssi.append(int(parts[5]))
                txbuf.append(int(parts[6]))
                noise.append(int(parts[7]))
                rem_noise.append(int(parts[8]))
                rxerrors.append(int(parts[9]))
                fixed.append(int(parts[10]))
        # plot SNR and rem_SNR over time
        plt.plot(time_usec, SNR, 'r-', label='SNR')
        plt.plot(time_usec, rem_SNR, 'b-', label='rem_SNR')
        # set y limits
        plt.ylim([0, 256])
        # grid on
        plt.grid()
        plt.xlabel('Time (us)')
        plt.ylabel('SNR')
        plt.title('SNR and rem_SNR over time')
        plt.legend()
        # plt.show()
        plt.savefig('plots/rocket_radio_status_SNR.png')
        plt.clf() # clear figure for next plot
        # plot rssi, rem_rssi, noise and rem_noise
        plt.plot(time_usec, rssi, 'r-', label='RSSI')
        plt.plot(time_usec, rem_rssi, 'b-', label='rem_RSSI')
        plt.plot(time_usec, noise, 'g-', label='Noise')
        plt.plot(time_usec, rem_noise, 'y-', label='rem_Noise')
        plt.ylim([0, 256])
        plt.grid()
        plt.xlabel('Time (us)')
        plt.ylabel('RSSI/Noise')
        plt.title('RSSI, rem_RSSI, Noise and rem_Noise over time')
        plt.legend()
        # plt.show()
        plt.savefig('plots/rocket_radio_status_RSSI_Noise.png')
        plt.clf() # clear figure for next plot
        # plot txbuf, rxerrors and fixed
        plt.plot(time_usec, txbuf, 'm-', label='TX Buffer')
        plt.plot(time_usec, rxerrors, 'c-', label='RX Errors')
        plt.plot(time_usec, fixed, 'k-', label='Fixed')
        plt.ylim([0, 256])
        plt.grid()
        plt.xlabel('Time (us)')
        plt.ylabel('TX/RX/Fixed')
        plt.title('TX Buffer, RX Errors and Fixed over time')
        plt.legend()
        # plt.show()
        plt.savefig('plots/rocket_radio_status_TX_RX_Fixed.png')
        plt.clf() # clear figure for next plot
        # count avg of all parameters
        avg_SNR = sum(SNR) / len(SNR) if SNR else 0
        avg_rem_SNR = sum(rem_SNR) / len(rem_SNR) if rem_SNR else 0
        avg_rssi = sum(rssi) / len(rssi) if rssi else 0
        avg_rem_rssi = sum(rem_rssi) / len(rem_rssi) if rem_rssi else 0
        avg_noise = sum(noise) / len(noise) if noise else 0
        avg_rem_noise = sum(rem_noise) / len(rem_noise) if rem_noise else 0
        avg_txbuf = sum(txbuf) / len(txbuf) if txbuf else 0
        avg_rxerrors = sum(rxerrors) / len(rxerrors) if rxerrors else 0
        avg_fixed = sum(fixed) / len(fixed) if fixed else 0
        # save to file
        with open('plots/status_avg.txt', 'w') as f:
                f.write(f"Rocket Radio Status Avg\n")
                f.write(f"Avg SNR: {avg_SNR}\n")
                f.write(f"Avg rem_SNR: {avg_rem_SNR}\n")
                f.write(f"Avg RSSI: {avg_rssi}\n")
                f.write(f"Avg rem_RSSI: {avg_rem_rssi}\n")
                f.write(f"Avg Noise: {avg_noise}\n")
                f.write(f"Avg rem_Noise: {avg_rem_noise}\n")
                f.write(f"Avg TX Buffer: {avg_txbuf}\n")
                f.write(f"Avg RX Errors: {avg_rxerrors}\n")
                f.write(f"Avg Fixed: {avg_fixed}\n")
        print(f"Avg SNR: {avg_SNR}")
        print(f"Avg rem_SNR: {avg_rem_SNR}")
        print(f"Avg RSSI: {avg_rssi}")
        print(f"Avg rem_RSSI: {avg_rem_rssi}")
        print(f"Avg Noise: {avg_noise}")
        print(f"Avg rem_Noise: {avg_rem_noise}")
        print(f"Avg TX Buffer: {avg_txbuf}")
        print(f"Avg RX Errors: {avg_rxerrors}")
        print(f"Avg Fixed: {avg_fixed}")

    with open(file_GS_msgs_received, 'r') as f:
        # vector of timestamps, vector of SNR, vector of rem_SNR
        time_usec = []
        SNR = []
        rem_SNR = []
        # vector of RSSI, rem_RSSI, Noise, rem_Noise
        rssi = []
        rem_rssi = []
        noise = []
        rem_noise = []
        txbuf = []
        rxerrors = []
        fixed = []
        for line in f:
            # devide by space
            parts = line.split(' ')
            if parts[0] == 'S':
                time_usec.append(int(parts[1]))
                SNR.append(int(parts[2]))
                rem_SNR.append(int(parts[3]))
                rssi.append(int(parts[4]))
                rem_rssi.append(int(parts[5]))
                txbuf.append(int(parts[6]))
                noise.append(int(parts[7]))
                rem_noise.append(int(parts[8]))
                rxerrors.append(int(parts[9]))
                fixed.append(int(parts[10]))
        # plot SNR and rem_SNR over time
        plt.plot(time_usec, SNR, 'r-', label='SNR')
        plt.plot(time_usec, rem_SNR, 'b-', label='rem_SNR')
        plt.ylim([0, 256])
        plt.grid()
        plt.xlabel('Time (us)')
        plt.ylabel('SNR')
        plt.title('SNR and rem_SNR over time')
        plt.legend()
        # plt.show()
        plt.savefig('plots/GS_radio_status_SNR.png')
        plt.clf() # clear figure for next plot
        # plot rssi, rem_rssi, noise and rem_noise
        plt.plot(time_usec, rssi, 'r-', label='RSSI')
        plt.plot(time_usec, rem_rssi, 'b-', label='rem_RSSI')
        plt.plot(time_usec, noise, 'g-', label='Noise')
        plt.plot(time_usec, rem_noise, 'y-', label='rem_Noise')
        plt.ylim([0, 256])
        plt.grid()
        plt.xlabel('Time (us)')
        plt.ylabel('RSSI/Noise')
        plt.title('RSSI, rem_RSSI, Noise and rem_Noise over time')
        plt.legend()
        # plt.show()
        plt.savefig('plots/GS_radio_status_RSSI_Noise.png')
        plt.clf() # clear figure for next plot
        # plot txbuf, rxerrors and fixed
        plt.plot(time_usec, txbuf, 'm-', label='TX Buffer')
        plt.plot(time_usec, rxerrors, 'c-', label='RX Errors')
        plt.plot(time_usec, fixed, 'k-', label='Fixed')
        plt.ylim([0, 256])
        plt.grid()
        plt.xlabel('Time (us)')
        plt.ylabel('TX/RX/Fixed')
        plt.title('TX Buffer, RX Errors and Fixed over time')
        plt.legend()
        # plt.show()
        plt.savefig('plots/GS_radio_status_TX_RX_Fixed.png')
        plt.clf() # clear figure for next plot
        # count avg of all parameters
        avg_SNR = sum(SNR) / len(SNR) if SNR else 0
        avg_rem_SNR = sum(rem_SNR) / len(rem_SNR) if rem_SNR else 0
        avg_rssi = sum(rssi) / len(rssi) if rssi else 0
        avg_rem_rssi = sum(rem_rssi) / len(rem_rssi) if rem_rssi else 0
        avg_noise = sum(noise) / len(noise) if noise else 0
        avg_rem_noise = sum(rem_noise) / len(rem_noise) if rem_noise else 0
        avg_txbuf = sum(txbuf) / len(txbuf) if txbuf else 0
        avg_rxerrors = sum(rxerrors) / len(rxerrors) if rxerrors else 0
        avg_fixed = sum(fixed) / len(fixed) if fixed else 0
        # save to file
        with open('plots/status_avg.txt', 'a') as f:
                f.write(f"\nGS Radio Status Avg\n")
                f.write(f"Avg SNR: {avg_SNR}\n")
                f.write(f"Avg rem_SNR: {avg_rem_SNR}\n")
                f.write(f"Avg RSSI: {avg_rssi}\n")
                f.write(f"Avg rem_RSSI: {avg_rem_rssi}\n")
                f.write(f"Avg Noise: {avg_noise}\n")
                f.write(f"Avg rem_Noise: {avg_rem_noise}\n")
                f.write(f"Avg TX Buffer: {avg_txbuf}\n")
                f.write(f"Avg RX Errors: {avg_rxerrors}\n")
                f.write(f"Avg Fixed: {avg_fixed}\n")
        print(f"Avg SNR: {avg_SNR}")
        print(f"Avg rem_SNR: {avg_rem_SNR}")
        print(f"Avg RSSI: {avg_rssi}")
        print(f"Avg rem_RSSI: {avg_rem_rssi}")
        print(f"Avg Noise: {avg_noise}")
        print(f"Avg rem_Noise: {avg_rem_noise}")
        print(f"Avg TX Buffer: {avg_txbuf}")
        print(f"Avg RX Errors: {avg_rxerrors}")
        print(f"Avg Fixed: {avg_fixed}")


    # =================== analize pings ===================

    # rocket side
    # load pings sent
    # struct for pings sent - timestamp and sequence num
    class PingP:
        def __init__(self, seq_num, timestamp):
            self.seq_num = seq_num

            self.timestamp = timestamp

            self.has_response = False
            self.response_time = None
            self.response_delay = None

    # create map for pings based on seq_num
    pings_map = {}

    with open(file_rocket_pings_sent, 'r') as f:
        for line in f:
            # parse line for timestamp and sequence num
            timestamp, seq_num = line.strip().split(' ')
            pings_map[seq_num] = PingP(seq_num, timestamp)

    # load received pings and match with sent pings
    max_delay_ping = 0
    with open(file_rocket_msgs_received, 'r') as f:
        for line in f:
            parts = line.split(' ')
            if parts[0] == 'P':
                time_received_usec = parts[1]
                time_sent_usec = parts[2]
                seq = parts[3]
                addr = parts[4]
                addr2 = parts[5]
                if addr == "1": # it is a response
                    if seq in pings_map:
                        pings_map[seq].has_response = True
                        pings_map[seq].response_time = time_received_usec
                        pings_map[seq].response_delay = int(time_received_usec) - int(time_sent_usec)
                        if pings_map[seq].response_delay > max_delay_ping:
                            max_delay_ping = pings_map[seq].response_delay
    
    # vector with pings that received response
    pings_times = []
    pings_seq_nums = []
    pings_delay = []
    pings_Y = []

    failed_pings_times = []
    failed_pings_seq_nums = []
    failed_pings_Y = []
    
    for ping in pings_map.values():
        if ping.has_response:
            pings_times.append(int(ping.timestamp)/1000) # convert to ms
            pings_delay.append(ping.response_delay/1000) # convert to ms
            pings_seq_nums.append(int(ping.seq_num))
            pings_Y.append(10)  # Add a value for Y
        else:
            failed_pings_times.append(int(ping.timestamp)/1000) # convert to ms
            failed_pings_seq_nums.append(int(ping.seq_num))
            failed_pings_Y.append(0)  # Add a value for Y

    # count avg delay, % packet loss and then save to file these and amount of pings, successfull and failed
    avg_delay = sum(pings_delay) / len(pings_delay) if pings_delay else 0
    packet_loss = ((len(failed_pings_times) / (len(pings_times) + len(failed_pings_times))) * 100) if (len(pings_times) + len(failed_pings_times)) > 0 else 0

    with open('plots/ping_stats.txt', 'w') as f:
        f.write(f"Rocket Ping Stats\n")
        f.write(f"Avg Delay: {avg_delay} ms\n")
        f.write(f"Packet Loss: {packet_loss}%\n")
        f.write(f"Total Pings: {len(pings_times) + len(failed_pings_times)}\n")
        f.write(f"Successful Pings: {len(pings_times)}\n")
        f.write(f"Failed Pings: {len(failed_pings_times)}\n")

    # plot delay over time
    plt.plot(pings_times, pings_delay, 'k-', label='Ping Response Delay (ms)')
    plt.plot(failed_pings_times, failed_pings_Y, 'r.', label='Failed Pings')
    plt.plot(pings_times, pings_Y, 'g.', label='Successful Pings')
    plt.ylim([0, max_delay_ping/1000])
    plt.grid()
    # plt resolution
    plt.gcf().set_size_inches(40, 20)
    plt.xlabel('Time (ms)')
    plt.ylabel('Ping Response Delay (ms)')
    plt.title('Ping Response Delay over Time (Rocket)')
    plt.legend()
    plt.savefig('plots/rocket_ping_response_delay.png')
    plt.clf() # clear figure for next plot

    # now for other side of the connection

    # create map for pings based on seq_num
    pings_map = {}

    with open(file_GS_pings_sent, 'r') as f:
        for line in f:
            # parse line for timestamp and sequence num
            timestamp, seq_num = line.strip().split(' ')
            pings_map[seq_num] = PingP(seq_num, timestamp)

    # load received pings and match with sent pings
    max_delay_ping = 0
    with open(file_GS_msgs_received, 'r') as f:
        for line in f:
            parts = line.split(' ')
            if parts[0] == 'P':
                time_received_usec = parts[1]
                time_sent_usec = parts[2]
                seq = parts[3]
                addr = parts[4]
                addr2 = parts[5]
                if addr == "1": # it is a response
                    if seq in pings_map:
                        pings_map[seq].has_response = True
                        pings_map[seq].response_time = time_received_usec
                        pings_map[seq].response_delay = int(time_received_usec) - int(time_sent_usec)
                        if pings_map[seq].response_delay > max_delay_ping:
                            max_delay_ping = pings_map[seq].response_delay
    
    # vector with pings that received response
    pings_times = []
    pings_seq_nums = []
    pings_delay = []
    pings_Y = []

    failed_pings_times = []
    failed_pings_seq_nums = []
    failed_pings_Y = []
    
    for ping in pings_map.values():
        if ping.has_response:
            pings_times.append(int(ping.timestamp)/1000) # convert to ms
            pings_delay.append(ping.response_delay/1000) # convert to ms
            pings_seq_nums.append(int(ping.seq_num))
            pings_Y.append(10)  # Add a value for Y
        else:
            failed_pings_times.append(int(ping.timestamp)/1000) # convert to ms
            failed_pings_seq_nums.append(int(ping.seq_num))
            failed_pings_Y.append(0)  # Add a value for Y
        
    # count avg delay, % packet loss and then save to file these and amount of pings, successfull and failed
    avg_delay = sum(pings_delay) / len(pings_delay) if pings_delay else 0
    packet_loss = ((len(failed_pings_times) / (len(pings_times) + len(failed_pings_times))) * 100) if (len(pings_times) + len(failed_pings_times)) > 0 else 0

    with open('plots/ping_stats.txt', 'a') as f:
        f.write(f"\nGS Ping Stats\n")
        f.write(f"Avg Delay: {avg_delay} ms\n")
        f.write(f"Packet Loss: {packet_loss}%\n")
        f.write(f"Total Pings: {len(pings_times) + len(failed_pings_times)}\n")
        f.write(f"Successful Pings: {len(pings_times)}\n")
        f.write(f"Failed Pings: {len(failed_pings_times)}\n")

    # plot delay over time
    plt.plot(pings_times, pings_delay, 'k-', label='Ping Response Delay (ms)')
    plt.plot(failed_pings_times, failed_pings_Y, 'r.', label='Failed Pings')
    plt.plot(pings_times, pings_Y, 'g.', label='Successful Pings')
    plt.ylim([0, max_delay_ping/1000])
    plt.grid()
    # plt resolution
    plt.gcf().set_size_inches(40, 20)
    plt.xlabel('Time (ms)')
    plt.ylabel('Ping Response Delay (ms)')
    plt.title('Ping Response Delay over Time (GS)')
    plt.legend()
    plt.savefig('plots/GS_ping_response_delay.png')
    plt.clf() # clear figure for next plot

    print("JD")


if __name__ == '__main__':
    main()