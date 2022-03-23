import socket

HOST = 'www.github.com'
PORT = 80
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))