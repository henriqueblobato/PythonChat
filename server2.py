import socket,select
PORT = 12345
socket_list = []
users = {}
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('', PORT))
server_socket.listen(5)
socket_list.append(server_socket)
while True:
    ready_to_read,ready_to_write,in_error = select.select(socket_list,[],[],0)
    for sock in ready_to_read:
        if sock == server_socket:
            client_connection, addr = server_socket.accept()
            socket_list.append(client_connection)
            client_connection.send("You are connected from:" + str(addr))
        else:
            try:
                data = sock.recv(2048)
                print data
                if data.startswith("#"):
                    users[data[1:].lower()] = client_connection
                    print "User " + data[1:] +" added."
                    client_connection.send("Your user detail saved as : "+str(data[1:]))
                elif data.startswith("@"):
                    for user in users:
                        users[user].send(data[data.index('@')+1:])
                    # index = data[1:data.index(':')].lower()
                    # users[index].send(data[data.index(':')+1:])
            
            except Exception as e:
                print('[!]', type(e), format(e))
                continue
server_socket.close()
