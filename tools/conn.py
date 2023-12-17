import os
import re
import socket


def find_ip():
    os.popen('chcp 65001')
    stream = os.popen('ipconfig')
    aus = stream.read().encode('cp1251').decode('cp866')
    target = re.findall(r'IPv4 Address.+: \d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}', aus)
    if len(target) == 0:
        print("Seems that you're not connected to the internet. Try again later!")
        return None
    else:
        return re.findall(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}', target[0])[0]


def open_port(host, port):
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        srv.bind((host, port))
    except OSError:
        return None
    return srv


def wait_incoming(srv):
    srv.listen(1)
    srv.settimeout(15)

    sock, addr = srv.accept()
    print('accepted')
    while True:
        print('receiving')
        pal = sock.recv(1024)
        if not pal:
            break
        print("Получено от %s:%s:" % addr, pal)
        break
    sock.send(b'CLEARED FOR FURTHER ACTIONS, TANGO-ALPHA-NOVEMBER-KILO-SIERRA')
    return sock, addr
