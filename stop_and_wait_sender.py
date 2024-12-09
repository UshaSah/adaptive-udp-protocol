
import socket


IP_ADDRESS = "127.0.0.1"
RECV_PORT = int(input("Enter the port number on which your receiver is running: "))

# create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# define server address and port
server_address = ("127.0.0.1", 8081)

message = "Hello, this is a UDP message!"

# send data

udp_socket.sendto(message.encode(), server_address)
print("Message sent!")

# close the socket
udp_socket.close()