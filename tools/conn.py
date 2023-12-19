import os
import random
import re
import socket

WRONGADDRESS = 3
REFUSED = 2
TIMEOUT = 1


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


def find_port():
    port = random.randint(30000, 40000)
    while not os.popen('netstat -ano | find ":' + str(port) + '"').read() == '':
        port = random.randint(30000, 40000)
    return port


def wait_incoming(host, port):
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        srv.bind((host, port))
        srv.listen(1)
    except OSError:
        return WRONGADDRESS
    sock, addr = srv.accept()
    return sock


def send_inquiry(host, port):
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.settimeout(5)
    try:
        srv.connect((host, port))
        print('sent')
        return srv
    except ConnectionRefusedError:
        return REFUSED
    except TimeoutError:
        return TIMEOUT
    except OSError:
        return WRONGADDRESS
