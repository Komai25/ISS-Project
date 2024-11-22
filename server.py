import socket
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


server_private_key = RSA.generate(2048)
server_public_key = server_private_key.publickey()
print(f"Server Public Key:\n{server_public_key.export_key().decode()}")


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)
print("Server is running...")

conn, addr = server_socket.accept()
print(f"Connection established with {addr}")

conn.send(server_public_key.export_key())

client_public_key = RSA.import_key(conn.recv(1024))
print("Received Client's Public Key.")

mode = conn.recv(1024).decode()
print(f"Client selected mode: {mode}")

if mode == "AES":
    key = get_random_bytes(32)
    conn.send(key)
elif mode == "RSA":
    print("RSA mode selected.")
elif mode == "None":
    print("No encryption selected.")

while True:
    # Receive encrypted message from Client
    data = conn.recv(1024)
    if not data:
        break

    if mode == "AES":
        iv = data[:16]
        encrypted_data = data[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_message = unpad(cipher.decrypt(encrypted_data), AES.block_size).decode()
    elif mode == "RSA":
        cipher_rsa = PKCS1_OAEP.new(server_private_key)
        decrypted_message = cipher_rsa.decrypt(data).decode()
    elif mode == "None":
        decrypted_message = data.decode()

    print(f"Client: {decrypted_message}")

    # Send Response to Client
    response = input("Server: ")
    if mode == "AES":
        cipher = AES.new(key, AES.MODE_CBC)
        encrypted_response = cipher.iv + cipher.encrypt(pad(response.encode(), AES.block_size))
    elif mode == "RSA":
        cipher_rsa = PKCS1_OAEP.new(client_public_key)
        encrypted_response = cipher_rsa.encrypt(response.encode())
    elif mode == "None":
        encrypted_response = response.encode()

    conn.send(encrypted_response)

conn.close()
server_socket.close()
