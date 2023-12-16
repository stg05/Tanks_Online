import os
import re


os.popen('chcp 65001')
stream = os.popen('ipconfig')
aus = stream.read().encode('cp1251').decode('cp866')
print(aus)
target = re.findall(r'IPv4 Address.+: \d{,3}.\d{,3}.\d{,3}.\d{,3}', aus)
print(target)
if len(target) == 0:
    print("Seems that you're not connected to the internet. Try again later!")
