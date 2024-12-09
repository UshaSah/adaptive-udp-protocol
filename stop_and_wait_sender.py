
import socket
import os

IP_ADDRESS = "127.0.0.1"
RECV_PORT = int(input("Enter the port number on which your receiver is running: "))

# create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# define server address and port
server_address = ("127.0.0.1", 8081)

# Configuration
IP_ADDRESS = "127.0.0.1"  # Receiver IP
RECV_PORT = 4010          # Receiver port
BUFFER_SIZE = 1000        # Maximum UDP packet size
WINDOW_SIZE = 5           # Static sliding window size
TIMEOUT = 5               # Timeout for retransmissions (in seconds)

# read the file and divide it into packets
file_path = "./message.txt"
file_size = os.path.getsize(file_path)

packets = []
sequence_number = 0
total_packets = 0

with open(file_path, "rb") as file:
    while True:
        chunk = file.read(BUFFER_SIZE - 4)
        if not chunk:
            break
        header = f"{sequence_number:04}".encode()
        packets.append((sequence_number, header + chunk))
        sequence_number += 1
        total_packets += 1



# send data

# udp_socket.sendto(message.encode(), server_address)
print("Message sent!")

# close the socket
udp_socket.close()