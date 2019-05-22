import json
import os,sys
import socket
s = socket.socket()
print "[I] Socket successfully created"
PORT = 12345
IP='192.168.1.176'
s.bind((IP, PORT))
print "[I] socket is binded to %s" % (PORT)
s.listen(5)
print "[I] socket is listening"
c, addr = s.accept()
try:
    while True:
        _data=c.recv(1024)
        data=json.loads(_data)
        # print(data)
        print '[I] Got connection from %s with data %s'%(addr,data)

        rpl={
            'msg':'200 OK'
        }
        c.send(json.dumps(rpl))
except KeyboardInterrupt:
    c.close()

