import socket
import threading


def display_data(direction, hex_data):
    try:
        # Convert hex to readable text
        readable_message = bytes.fromhex(hex_data).decode('utf-8')
    except Exception as e:
        readable_message = f"Could not decode message: {e}"

    print(f"[{direction}] Hex: {hex_data}")
    print(f"[{direction}] Text: {readable_message}")


def forward_data(source, destination, direction):
    try:
        while True:
            data = source.recv(1024)
            if not data:
                break

            hex_data = data.hex()  
            display_data(direction, hex_data) 

            destination.sendall(data)
    except Exception as e:
        print(f"Error in {direction}: {e}")
    finally:
        source.close()
        destination.close()


def proxy_listener():
    # Proxy configuration
    proxy_port = 9999
    target_host = 'localhost'
    target_port = 12345

    listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener_socket.bind(('localhost', proxy_port))
    listener_socket.listen(1)
    print(f"Proxy listening on port {proxy_port}...")

    try:
        conn, addr = listener_socket.accept()
        print(f"Connection established with {addr} (Client)")

        # Connect to the actual server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((target_host, target_port))
        print(f"Connected to server at {target_host}:{target_port}")

        # Start threads to forward data
        threading.Thread(target=forward_data, args=(conn, server_socket, "Client -> Server"), daemon=True).start()
        threading.Thread(target=forward_data, args=(server_socket, conn, "Server -> Client"), daemon=True).start()

        while True:
            pass  # Keep the proxy running
    except KeyboardInterrupt:
        print("\nStopping the proxy listener.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        listener_socket.close()

proxy_listener()

