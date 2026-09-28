import socket
import threading
import sys

def receive_messages(sock):
    """Thread function dedicated to listening for incoming messages."""
    while True:
        try:
            # Receive data from the server
            data = sock.recv(1024)
            if not data:
                print("\n[Disconnected] Server closed the connection.")
                break
            print(f"\n[Received]: {data.decode('utf-8')}")
        except ConnectionResetError:
            print("\n[Error] Connection reset by peer.")
            break
        except Exception as e:
            print(f"\n[Error] Socket error: {e}")
            break
            
    print("Exiting receive thread...")
    sock.close()
    sys.exit()

def send_messages(sock, client_name):
    print("Type your message and press Enter. Type 'exit' to quit.")
    while True:
        try:
            msg = input()
            if msg.lower() == 'exit':
                print("Closing connection...")
                break
            if msg: # Ensure we don't send empty strings
                msg = f'[{client_name}] ' + msg
                sock.sendall(msg.encode('utf-8'))
        except Exception as e:
            print(f"[Error] Failed to send message: {e}")
            break
            
    sock.close()

def main():
    HOST = '127.0.0.1'  # Localhost, change accordingly on different client device
    PORT = 9999        # non-privileged port

    name = input('Dien ten cua ban: ')
    # Initialize TCP Streaming IPv4 Socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")
    except ConnectionRefusedError:
        print("Could not connect. Is the server running?")
        return

    # Start the RECEIVE thread
    # Daemon=True ensures this background thread shuts down when the main script exits
    recv_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
    recv_thread.start()

    # Use the main thread for the SEND function
    send_messages(client_socket, name)

if __name__ == '__main__':
    main()