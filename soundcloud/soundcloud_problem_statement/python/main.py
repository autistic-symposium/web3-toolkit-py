import socket
import threading

EVENT_PORT = 9090
CLIENT_PORT = 9099
client_pool = {}
follow_registry = {}
seq_no_to_message = {}

def event_server():
    last_seq_no = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("127.0.0.1", EVENT_PORT))
        server.listen()
        print("Listening for events on %d" % EVENT_PORT)
        while True:
            event_socket, address = server.accept()
            print('Accepted connection from {}:{}'.format(address[0], address[1]))
            with event_socket:
                with event_socket.makefile() as socket_file:
                    for payload_line in socket_file:
                        payload = payload_line.strip()
                        print("Message received: %s" % payload)
                        payload_parts = payload.split("|")

                        seq_no_to_message[int(payload_parts[0])] = payload_parts

                        while last_seq_no + 1 in seq_no_to_message:
                            next_seq_no = last_seq_no + 1
                            next_message = seq_no_to_message[next_seq_no]
                            del seq_no_to_message[next_seq_no]

                            kind = next_message[1]
                            next_payload = "|".join(next_message)

                            if kind == "F":
                                from_user_id = int(next_message[2])
                                to_user_id = int(next_message[3])

                                if to_user_id not in follow_registry:
                                    follow_registry[to_user_id] = set([])
                                follow_registry[to_user_id].add(from_user_id)

                                #if to_user_id in client_pool:
                                #    client_pool[to_user_id].sendall(bytes(next_payload + "\n", "UTF-8"))

                            elif kind == "U":
                                from_user_id = int(next_message[2])
                                to_user_id = int(next_message[3])

                                if to_user_id not in follow_registry:
                                    follow_registry[to_user_id] = set([])
                                follow_registry[to_user_id].remove(from_user_id)

                            elif kind == "P":
                                to_user_id = int(next_message[3])

                                if to_user_id in client_pool:
                                    client_pool[to_user_id].sendall(bytes(next_payload + "\n", "UTF-8"))

                            elif kind == "B":
                                for client_id in client_pool:
                                    client_pool[client_id].sendall(bytes(next_payload + "\n", "UTF-8"))

                            elif kind == "S":
                                from_user_id = int(next_message[2])

                                if from_user_id in follow_registry:
                                    for follower in follow_registry[from_user_id]:
                                        if follower in client_pool:
                                            client_pool[follower].sendall(bytes(next_payload + "\n", "UTF-8"))

                            last_seq_no = next_seq_no

def client_connection_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("127.0.0.1", CLIENT_PORT))
        server.listen()
        print("Listening for client requests on %d" % CLIENT_PORT)
        while True:
            client_socket, address = server.accept()
            with client_socket.makefile() as f:
                user_id_string = f.readline()
                if user_id_string:
                    user_id = int(user_id_string)
                    client_pool[user_id] = client_socket
                    print("User connected: %d (%d total)" % (user_id, len(client_pool)))

if __name__ == "__main__":
    thread1 = threading.Thread(target=event_server)
    thread1.start()

    thread2 = threading.Thread(target=client_connection_server)
    thread2.start()

    thread1.join()
    thread2.join()
