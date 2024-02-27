import socket
import threading
import rsa

public_key, private_key = rsa.newkeys(1024)
public_key_partner = None

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("172.31.114.173", 9999))

public_key_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
client.send(public_key.save_pkcs1("PEM"))

def send_msg(c):
    while True:
        message = input("")
        c.send(rsa.encrypt(message.encode(), public_key_partner))
        print("Member2: " + message)

def recv_msg(c):
    while True:
        print("Member2: " + rsa.decrypt(c.recv(1024), private_key).decode())

threading.Thread(target=send_msg, args=(client,)).start()
threading.Thread(target=recv_msg, args=(client,)).start()
