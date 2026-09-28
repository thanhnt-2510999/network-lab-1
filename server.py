import socket
import threading

client_list = {}
lock = threading.Lock()

def handle_client(conn, addr):
    print(f"Connection from: {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:  # empty bytes means the client closed the connection
                break
            with lock:
                targets = list(client_list.items())
            for target, write_lock in targets:
                try:
                    with write_lock:
                        target.sendto(data, target.getpeername())
                except OSError:
                    pass
            # conn.sendall(data)  # echo received data back to the client
    except (ConnectionResetError, BrokenPipeError) as e:
        print(f"Connection error with {addr}: {e}")
    finally:
        conn.close()


def server_program():
    host = '0.0.0.0'  # loopback address for local testing
    port = 9999

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4 TCP socket
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # allow port reuse immediately after server shutdown
    server_socket.bind((host, port))
    server_socket.listen(10)  # queue up to 10 connection requests
    print(f"Server listening on {host}:{port}")

    try:
        while True:
            conn, addr = server_socket.accept()
            with lock:
                client_list[conn] = threading.Lock()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
            print(f"Active connections: {threading.active_count() - 1}")
    except KeyboardInterrupt:
        print("Server shutting down")
    finally:
        server_socket.close()


if __name__ == '__main__':
    server_program()