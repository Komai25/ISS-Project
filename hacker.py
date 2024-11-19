import socket

# إعداد العميل
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

print("Connected to the server. Ready to see encrypted data.")

while True:
    # إرسال الرسالة
    message = input("Client (plaintext): ")
    client_socket.send(message.encode())

    # استقبال الرد المشفر من الخادم
    encrypted_response = client_socket.recv(1024)
    print(f"Encrypted response from server: {encrypted_response.hex()}")

client_socket.close()
