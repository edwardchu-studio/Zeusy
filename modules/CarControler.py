import PCF8591 as ADC
import time

class CarController(object):
    def __init__(self):
        ADC.setup(0x48)
        self.STATUS_PANE=['still','forward','rear','left','right','x']

        self.CURRENT_STATUS=''

    def move_forward(self,speed=0):
        print("car moving forward with speed",speed)
    def move_backward(self,speed=0):
        print("car moving backward with speed:",speed)
    def turn_right(self):
        print("car turnning right")
    def turn_left(self):
        print("car turnning left")
    def X_pressed(self):
        print("X pressed!")

    def fetch_current_coor(self):
        return (ADC.read(0)-128,ADC.read(1)-128,ADC.read(2))
    def loop(self):
        while(True):
            y,x,p=self.fetch_current_coor()
            if y<0:
                self.move_backward()
            elif y>0:
                self.move_forward()
            if x<0:
                self.turn_left()
            elif x>0:
                self.turn_right()
            if p==0:
                self.X_pressed()
    def destroy(self):
        print("Controller Exit!")

    def listen(self,debug=False):
        print("Initilization Finished")
        try:
            self.loop()
        except KeyboardInterrupt:
            destroy()
    
if __name__=='__main__':
    CC=CarController()
    CC.listen()
