import socket
# from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

key = client_socket.recv(1024)
print(f"Recevied key from server. Key received: {key.hex()}") #key.hex()

while True:
    message = input("Client: ")
    cipher = AES.new(key,AES.MODE_CBC)
    encrypted_message = cipher.iv + cipher.encrypt(pad(message.encode(),AES.block_size))
    client_socket.send(encrypted_message)


    encrypted_response = client_socket.recv(1024)
    iv = encrypted_response[:16]
    encrypted_data = encrypted_response[16:]
    cipher = AES.new(key, AES.MODE_CBC,iv)
    decrypted_response = unpad(cipher.decrypt(encrypted_data),AES.block_size).decode()
    print(f"Server: {decrypted_response}")

client_socket.close()
