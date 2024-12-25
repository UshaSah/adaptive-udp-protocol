
import socket
import os

IP_ADDRESS = "127.0.0.1"

RECV_PORT = int(input("Enter the Port number on which your receiver is running: "))
server_address = ("127.0.0.1", RECV_PORT)
BUFFER_SIZE = 1500
WINDOW_SIZE = 5
TIMEOUT = 2


udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((IP_ADDRESS, 8081))
udp_socket.settimeout(TIMEOUT)

file_path = "./message.txt"

with open(file_path, "rb") as file:
    data = file.read()
    
packets = [
    f"{i+1}|".encode() + data[i * (BUFFER_SIZE - 4):(i + 1) * (BUFFER_SIZE - 4)]
    for i in range((len(data) + BUFFER_SIZE - 5) // (BUFFER_SIZE - 4))
]



num_packets = len(packets)
print(f"Total number of packets: {num_packets}")
seq_num = 1



def slide_window(seq_num):
    window = []
    for i in range(seq_num -1, min(seq_num - 1 + WINDOW_SIZE, num_packets)):
        window.append(packets[i])
    # print(len(window))
    return window

def sending_packet():
    
    global seq_num
    
    while seq_num < num_packets:
        window = slide_window(seq_num)
        last_header,_ = window[4].split(b"|", 1)
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
                    seq_num += 5
                    break
        except socket.timeout:
            print("Timeout occurred. Retransmitting unacknowledged packets...")

        # If all packets are acknowledged, break
        if seq_num >= num_packets:
            break

    print("File transfer complete!")

sending_packet()

udp_socket.close()
