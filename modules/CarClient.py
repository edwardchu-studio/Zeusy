import socket
import json
from CarControler import CarController
CC=CarController()
CCgen=CC.listen_gen()
s = socket.socket()
IP='192.168.1.179'
PORT = 12345
s.connect((IP,PORT))
try:
    while(True):
        y,x,p=next(CCgen)
        _data={
            'speed':0,
            'status':(y,x,p),
        }
        data=json.dumps(_data)
        s.send(data)
        rpl=s.recv(1024)
        print(rpl)
except KeyboardInterrupt:
    s.close()
