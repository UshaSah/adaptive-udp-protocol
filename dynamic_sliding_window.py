
# In this part, implement a “Dynamic Sliding Window” service at the sender. Assume that the
# receive window (rwnd) at the receiver is sufficiently large.
# Thus, the sliding window size is determined by cwnd at the sender.
# Implement slow start and congestion avoidance as defined in TCP Tahoe.
# Start with the initial congestion window of 1 packet and ssthresh of 16 packets.
# You should use 5 seconds as the initial timeout value and then use a dynamic timeout based on the
# procedure described in Section 3.5.3 of the textbook to transfer the message.tx
import socket
import time
import os
import sys

# global parameters

IP_ADDRESS = "receiver"
# RECV_PORT = int(input("Enter the Port numbr on which your receiver is running: "))
RECV_PORT = 4010
BUFFER_SIZE = 1500
TIMEOUT = 5  # Initial timeout value in seconds
INITIAL_CWND = 1  # Initial congestion window size (in packets)
SSTHRESH = 16  # Slow start threshold
ALPHA = 0.125  # Alpha for SRTT calculation
BETA = 0.25  # Beta for RTTVAR calculation
# WINDOW_SIZE = 1
cwnd = 1

# if len(sys.argv) < 2:
#     print("Usage: python dynamic_sliding_window.py <RECV_PORT>")
#     sys.exit(1)

# RECV_PORT = int(sys.argv[1])

# Create UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.settimeout(TIMEOUT)

# read the file and create packets
file_path = "message.txt"
with open(file_path, "rb") as file:
    data = file.read()
    
packets = [
    f"{i+1}|".encode() + data[i * (BUFFER_SIZE - 4):(i + 1) * (BUFFER_SIZE - 4)]
    for i in range((len(data) + BUFFER_SIZE - 5) // (BUFFER_SIZE - 4))
]

num_packets = len(packets)
print(f"Total number of packets: {num_packets}")
seq_num = 1
ssthresh = SSTHRESH
cwnd = INITIAL_CWND


def slide_window(seq_num, cwnd):
    window = []
    for i in range(seq_num -1, min(seq_num - 1 + cwnd, num_packets)):
        window.append(packets[i])
    # print(len(window))
    return window

def sending_packet():    
    global seq_num, cwnd, ssthresh
    
    while seq_num < num_packets:
        window = slide_window(seq_num, cwnd)
        last_header,_ = window[-1].split(b"|", 1)
        last_pkt = int(last_header.decode())
        for packet in window:
            udp_socket.sendto(packet, (IP_ADDRESS, RECV_PORT)) 
            packet_no, content = packet.split(b"|", 1)
            # packet_no = int(packet_no.decode())    
            print(f"Sent packet: {packet_no.decode()}")  # Log the sequence number
        try:
           while True:
                ack_data, _ = udp_socket.recvfrom(BUFFER_SIZE)
                ack_num = int(ack_data.decode())
                print(f"Received ACK for packet {ack_num}")
                
                if ack_num == -1:
                    print("Receiver reported a sequence number error. Retransmitting current window.")
                    slide_window(seq_num)  # Retransmit the entire current window
                    break
                # if 1 <= ack_num <= num_packets:
                #     ack_list[ack_num - 1] = True  
                # Slide the base forward for all acknowledged packets
                if ack_num == last_pkt:                   
                    seq_num += cwnd 
                    
                    # slow start
                    if cwnd < ssthresh:
                        cwnd *= 2
                    
                    else:
                        cwnd += 1 
                    
                    print(f"CWND: {cwnd}")
                    break
        except socket.timeout:
            print("Timeout occurred. Retransmitting unacknowledged packets...")
            ssthresh = max(1, cwnd / 2)
            cwnd = 1
       
        # If all packets are acknowledged, break
        if seq_num >= num_packets:
            break
        
    print("File transfer complete!")

sending_packet()

udp_socket.close()
