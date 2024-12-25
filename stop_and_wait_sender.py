
import socket
import os


RECV_PORT = int(input("Enter the port number on which your receiver is running: "))

# Configuration
IP_ADDRESS = "127.0.0.1"  # Receiver IP
BUFFER_SIZE = 1000        # Maximum UDP packet size
WINDOW_SIZE = 5           # Static sliding window size
TIMEOUT = 5               # Timeout for retransmissions (in seconds)

# create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# define server address and port
server_address = ("127.0.0.1", RECV_PORT)
udp_socket.settimeout(TIMEOUT)

# read the file and divide it into packets
file_path = "./message.txt"
file_size = os.path.getsize(file_path)

packets = []
total_packets = 0

# read file and split into packets
with open(file_path, "rb") as file:
    data = file.read()

packets = [data[i:i + BUFFER_SIZE - 4] for i in range(0, len(data), BUFFER_SIZE - 4)]

def stop_and_wait():
    for sequence_number, packet in enumerate(packets):
        while True:
            try:
                # create packet with sequence number header
                header = f"{sequence_number}|".encode()
                udp_socket.sendto(header + packet, server_address)
                print(f"Sent packet: {sequence_number}")
                
                # wait for acknowledgement
                ack, _ = udp_socket.recvfrom(BUFFER_SIZE)
                ack_num = int(ack.decode())
                print(f"Received ACK for packet {ack_num}")
                
                if ack_num == sequence_number:
                    break
            except socket.timeout:
                print(f"Timeout for packet {sequence_number}. Retrying...")
                
stop_and_wait()
print("File transfer complete!")

# close the socket
udp_socket.close()