
#
#
#   Código comentado do servidor
#
#

# Importação das bibliotecas necessárias
import socket,select
# Escolha da porta padrão de conexão do servidor
PORT = 12345
# Variável que armazenará a lista de sockets
socket_list = []
# Variável que relacionará os usuários com suas respectivas conexões. A estrutura de dados dictionary no Python é responsável por guardar a instância de conexão para cada usuário
users = {}
# Criação da instância do socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Configuração de socket TCP
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Configuração de porta em localhost
server_socket.bind(('', PORT))
# Definição máxima de usuários simultâneos
server_socket.listen(5)
# Colocando o servidor na lista de sockets
socket_list.append(server_socket)
# Começando o loop infinito responsável pelo recebimento das conexões
while True:
    # Lendo toda conexão TCP que chega pela porta especificada
    ready_to_read,ready_to_write,in_error = select.select(socket_list,[],[],0)
    # Checando se o conteúdo existe
    for sock in ready_to_read:
        # Checando se o conteúdo é um socket válido (do mesmo tipo)
        if sock == server_socket:
            # Aceitando a conexão TCP
            client_connection, addr = server_socket.accept()
            # Salvando a nova conexão na lista de sockets
            socket_list.append(client_connection)
            # Envio da mensagem de verificação para o usuário
            client_connection.send("You are connected from:" + str(addr))
        else:
            # Caso o formato recebido não seja um início de handshake, essa condição é alcançada
            try:
                # Capturando os dados em 2048 bytes da conexão
                data = sock.recv(2048)
                # Se o dado começar com '#' significa que temos um novo usuário se conectando
                if data.startswith("#"):
                    # Na estrutura de dados dict, adicione seu nome como chave e sua conexão como valor
                    users[data[1:].lower()] = client_connection
                    # Mostre o nome do novo usuário conectado
                    client_connection.send("Your user detail saved as : "+str(data[1:]))
                # Se o dado iniciar com '@' significa que é uma mensagem
                elif data.startswith("@"):
                    # Para cada usuário conectado na lista de usuários cadastrados
                    for user in users:
                        # Enviando a mensagem recebida para toda conexão armazenada de conexões anteriores
                        users[user].send(data[data.index('@')+1:])
                    # index = data[1:data.index(':')].lower()
                    # users[index].send(data[data.index(':')+1:])
            
            except Exception as e:
                print('[!]', type(e), format(e))
                continue
# Fechamento do socket do servidor
server_socket.close()


#
#
#   Código comentado do cliente
#
#

# Importação da biblioteca
import socket
# Criação do socket, instância
client_socket = socket.socket()
# Especificação da porta dos servidor
port = 12345
# Início de conexão com o servidor
client_socket.connect(('127.0.0.1',port))
# Recebimento da mensagem de escolha de nome de usuário
recv_msg = client_socket.recv(1024)
# Exibição da mensagem
print recv_msg
# Escolha do nome de usuário
send_msg = raw_input("Enter your user name(prefix with #):")
# Envio do nome escolhido para o servidor
client_socket.send(send_msg)
# Loop infinito
while True:
    # Recebendo os dados do servidor
    recv_msg = client_socket.recv(1024)
    # Exibição na tela para o usuário
    print recv_msg
    # Campo para o usuário digitar a mensagem a ser exibida em broadcast, para todos os outros usuários conectados
    send_msg = raw_input("Message (with @): ")
    # Envio dos dados para o servidor
    client_socket.send(send_msg)
# Fechamento da conexão 
client_socket.close()
