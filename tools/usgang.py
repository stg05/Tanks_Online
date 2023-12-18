import socket, string

HOST = "127.0.0.1"  # localhost
PORT = 3333
srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    srv.connect((HOST, PORT))
    print('connected')
    #srv.send(b'TANGO-ALPHA-NOVEMBER-KILO-SIERRA CHECKING IN...')
    while True:
        pal = srv.recv(1024)
        if not pal:
            break
        print("Получено от %s:" % pal)
        srv.close()
        break
except ConnectionRefusedError:
    print('Connection refused. Try again later!')
