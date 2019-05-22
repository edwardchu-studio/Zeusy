import socket
s = socket.socket()
IP='127.0.0.1'
PORT = 12345
s.connect((IP,PORT))

data=s.recv(1024)

# close the connection 
s.close()        