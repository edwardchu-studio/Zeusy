import json
import os,sys
import socket
from PiCar import PiCar
car=PiCar(debug=True)
s = socket.socket()
print "[I] Socket successfully created"
PORT = 12345
IP='192.168.1.179'
s.bind((IP, PORT))
print "[I] socket is binded to %s" % (PORT)
s.listen(5)
print "[I] socket is listening"
c, addr = s.accept()
car.back_wheels.speed=0.
try:
    speed = 0.
    max_a=10.
    max_speed=99.
    while True:
        _data=c.recv(1024)
        data=json.loads(_data)
        # print(data)
        print '[I] Got connection from %s with data %s'%(addr,data)
        y,x,p=data['status']
        y,x,p=map(float,[y,x,p])

        car.front_wheels.turn(car.front_wheels.angle['straight']+(int(x*car.front_wheels.turning_max)))

        if y==0:
            speed=0.
        elif abs(speed)<max_speed:
            speed+=int(y*max_a)

        if speed>0:
            speed=min(speed,max_speed)
        else:
            speed=max(-max_speed,speed)
        if speed>=0:
            car.back_wheels.forward()
            car.back_wheels.speed=abs(speed)
        else:
            car.back_wheels.backward()
            car.back_wheels.speed=abs(speed)
        rpl={
            'msg':'200 OK'
        }
        c.send(json.dumps(rpl))
except:
    car.back_wheels.speed=0.
    c.close()
    raise

