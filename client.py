import socket
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad


client_private_key = RSA.generate(2048)
client_public_key = client_private_key.publickey()
print(f"Client Public Key:\n{client_public_key.export_key().decode()}")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))


server_public_key = RSA.import_key(client_socket.recv(1024))
print("Received Server's Public Key.")


client_socket.send(client_public_key.export_key())


mode = input("Choose encryption mode (AES/RSA/None): ")
client_socket.send(mode.encode())

if mode == "AES":

    key = client_socket.recv(32)
    print("Received AES key from server.")
elif mode == "RSA":
    print("RSA mode selected.")
elif mode == "None":
    print("No encryption selected.")

while True:

    message = input("Client: ")
    if mode == "AES":
        cipher = AES.new(key, AES.MODE_CBC)
        encrypted_message = cipher.iv + cipher.encrypt(pad(message.encode(), AES.block_size))
    elif mode == "RSA":
        cipher_rsa = PKCS1_OAEP.new(server_public_key)
        encrypted_message = cipher_rsa.encrypt(message.encode())
    elif mode == "None":
        encrypted_message = message.encode()

    client_socket.send(encrypted_message)


    data = client_socket.recv(1024)
    if mode == "AES":
        iv = data[:16]
        encrypted_data = data[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_response = unpad(cipher.decrypt(encrypted_data), AES.block_size).decode()
    elif mode == "RSA":
        cipher_rsa = PKCS1_OAEP.new(client_private_key)
        decrypted_response = cipher_rsa.decrypt(data).decode()
    elif mode == "None":
        decrypted_response = data.decode()

    print(f"Server: {decrypted_response}")

client_socket.close()
