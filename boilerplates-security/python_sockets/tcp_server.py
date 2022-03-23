import socket
import threading


BIND_IP = '0.0.0.0'
BIND_PORT = 9090


def handle_client(client_socket):
   request = client_socket.recv(1024)
 
   print(f'[*] Received: {request}')
 
   client_socket.send('ACK')
   client_socket.close()

def tcp_server():
   
   server = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
   server.bind(( BIND_IP, BIND_PORT))
   server.listen(5)
 
   print(f'[*] Listening on {BIND_IP}, {BIND_PORT}')
   while 1:
       client, addr = server.accept()
       print(f'[*] Accepted connection: {addr[0]}:{addr[1]}')
      
       client_handler = threading.Thread(target=handle_client, args=    (client,))
       client_handler.start()

       
if __name__ == '__main__':
    tcp_server()