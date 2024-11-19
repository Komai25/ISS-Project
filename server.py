import socket
# from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad



key = get_random_bytes(32)
print(f'Server Key: {key.hex()}')

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)

print(f"Server is running... Key: {key.hex()}")

conn, addr = server_socket.accept()
print(f"Connection established with {addr}")


# Send the Key to the Client
conn.send(key)

while True:
    # recive message 
    encrypted_message = conn.recv(1024)
    if not encrypted_message:
        break
    
    # Decrypt message
    iv = encrypted_message[:16]
    encrypted_data = encrypted_message[16:]
    cipher = AES.new(key, AES.MODE_CBC,iv)
    decrypted_message = unpad(cipher.decrypt(encrypted_data),AES.block_size).decode()
    print (f"Client: {decrypted_message}")

    #Send message 
    response = input("Server: ")
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    encrypted_response = iv + cipher.encrypt(pad(response.encode(), AES.block_size))
    conn.send(encrypted_response)

    

conn.close()
server_socket.close()
