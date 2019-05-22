# import CarControler
import os,sys
import socket
s = socket.socket()
print "[I] Socket successfully created"
port = 12345
s.bind(('', port))
print "[I] socket is binded to %s" % (port)
s.listen(5)
print "[I] socket is listening"
while True:
    c, addr = s.accept()
    print '[I] Got connection from', addr
    c.send('Thank you for connecting')

    c.close()