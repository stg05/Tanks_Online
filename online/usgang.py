import socket, string


HOST = "127.0.0.1" # localhost
PORT = 3333
srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.connect((HOST, PORT))
print('connected')
srv.send(b'tuna')
