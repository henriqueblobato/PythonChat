import socket
client_socket = socket.socket()
port = 12345
client_socket.connect(('127.0.0.1',port))

recv_msg = client_socket.recv(1024)
print recv_msg

send_msg = raw_input("Enter your user name(prefix with #):")
client_socket.send(send_msg)

while True:
    recv_msg = client_socket.recv(1024)
    print recv_msg
    # send_msg = raw_input("Send your message in format [@user:message] ")
    send_msg = raw_input("Message with (@): ")
    client_socket.send(send_msg)
client_socket.close()
