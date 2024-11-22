# **Socket Listener for Monitoring Client-Server Communication**

This project demonstrates how to intercept and log messages between a **client** and a **server** over a TCP connection using sockets. It includes encryption support, allowing you to observe communication in both raw hexadecimal format and decoded text.

---

## **Project Overview**

The system consists of three main components:

1. **Server**: A simple server that listens for incoming connections from the client. It can handle different encryption modes (AES, RSA, or no encryption).
2. **Client**: The client establishes a connection to the server, sends messages, and handles encryption as selected by the user.
3. **Listener**: A passive listener that intercepts the messages exchanged between the client and server. It logs the data in both hexadecimal and decoded text formats.

---

## **Features**

- **Socket Communication**: The client and server communicate using TCP sockets.
- **Encryption Modes**: The client and server support three modes:
  - **AES**: Symmetric encryption using AES (Advanced Encryption Standard).
  - **RSA**: Asymmetric encryption using RSA.
  - **None**: No encryption.
- **Hexadecimal Logging**: The listener logs all data as hexadecimal values, providing visibility into the raw data exchanged.
- **Message Decoding**: If possible, the listener decodes hexadecimal data into readable text.

---

## **Requirements**

- Python 3.x
- The following Python libraries:
  - `pycryptodome`: For encryption/decryption operations.
  - `socket`: For creating the server, client, and listener sockets.

To install the required libraries, run:

```bash
pip install pycryptodome
```

---

## **Usage**

### **1. Start the Listener**

First, run the **listener**. It will listen for incoming messages and log them.

```bash
python listener.py
```

The listener will print the raw data as hexadecimal and, if possible, decode it into readable text.

### **2. Start the Server**

Next, run the **server** to start accepting connections.

```bash
python server.py
```

The server will print its public key and wait for a client to connect.

### **3. Start the Client**

Finally, run the **client**, which will connect to the server, select an encryption mode, and send messages.

```bash
python client.py
```

You’ll be prompted to choose the encryption mode (AES, RSA, or None). The client will send messages to the server, and the listener will capture and display the communication.

---

## **How It Works**

1. **Server**:
   - The server generates its public and private RSA keys.
   - It waits for a client to connect and establishes communication using a specified encryption mode.
   - The server decrypts incoming messages, processes them, and sends a response back to the client.

2. **Client**:
   - The client generates its public and private RSA keys.
   - It connects to the server, sends its public key, and selects the encryption mode.
   - The client encrypts messages using the selected mode and sends them to the server.

3. **Listener**:
   - The listener listens on port `9999` and logs data exchanged between the client and the server.
   - It captures all messages in **hexadecimal format** and tries to decode them into human-readable text.
   - The listener does **not interfere** with the communication but simply captures and logs the data for analysis.

---

## **Example Communication**

- **Client** sends:
  - `Hello` (encoded as `48656c6c6f` in hexadecimal).

- **Listener** logs:
  - `[Client -> Server] Hex: 48656c6c6f`
  - `[Client -> Server] Text: Hello`

- **Server** responds with:
  - `Hi` (encoded as `4869` in hexadecimal).

- **Listener** logs:
  - `[Server -> Client] Hex: 4869`
  - `[Server -> Client] Text: Hi`

---

## **Encryption Modes**

The encryption mode can be selected when prompted by the client. Here’s how each mode works:

- **AES Mode**:
  - The client and server exchange a secret 256-bit AES key.
  - Messages are encrypted using AES in CBC (Cipher Block Chaining) mode.

- **RSA Mode**:
  - The client and server exchange public keys.
  - Messages are encrypted with the recipient's public key and decrypted using their private key.

- **None**:
  - No encryption is applied. Messages are sent as plaintext.

---

## **Known Issues**

- **Message Decoding**: If the listener intercepts binary or encrypted data, it may not be able to decode it into readable text, but it will still log the hexadecimal representation.

---

## **License**

This project is licensed under the MIT License. See the LICENSE file for more details.

---

## **Acknowledgements**

- **PyCryptodome**: Used for encryption and decryption operations. [PyCryptodome GitHub](https://github.com/Legrandin/pycryptodome)
- **Socket Programming**: Python's built-in `socket` library is used to establish connections and handle data transmission.

---
