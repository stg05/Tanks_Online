
import socket, string

HOST = "" # localhost
PORT = 3333
srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.bind((HOST, PORT))

print(f"Слушаю порт {PORT}")
srv.listen(1)
sock, addr = srv.accept()
print('accepted')
while True:
    pal = sock.recv(1024)
    if not pal:
        break
    print("Получено от %s:%s:" % addr, pal)
    sock.close()
    break
