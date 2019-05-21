import PCF8591 as ADC
import time
import json
import os,sys

class CarController(object):
    def __init__(self):
        ADC.setup(0x48)
        self.STATUS_PANE=['still','forward','rear','left','right','x']
        self.oy,self.ox,self.op=ADC.read(0),ADC.read(1),ADC.read(2)
        self.CURRENT_STATUS=''
        self.ground_threshold=0.03
        if os.path.exists('ground.json'):
            self.ground=json.load(open('ground.json'))
        else:
            print("Please adjust the ground")
            self.ground=self.adjust_ground()
        
        self.CUR_SPEED=0.0
        self.CUR_DIR=(0.,0.)
        self.MAX_SPEED=120

    def adjust_ground(self):
        print("Ground Adjustment Begin!")
        print("Please draw circle using the joy stick three times in 15s.")
        ys,xs,ps=[],[],[]
        t=time.time()
        while(time.time()-t<15):
            ys.append(ADC.read(0))
            xs.append(ADC.read(1))
            ps.append(ADC.read(2))
        min_y,max_y=min(ys),max(ys)
        min_x,max_x=min(xs),max(xs)
        min_p,max_p=min(ps),max(ps)
        log={
                'y':(min_y,max_y),
                'x':(min_x,max_x),
                'p':(min_p,max_p)
                }
        json.dump(log,open('ground.json','w'))
        del ys
        del xs
        del ps

        return log

    def move_forward(self,speed=0):
        if self.CUR_SPEED<self.MAX_SPEED:
            self.CUR_SPEED+=1
        print("car moving forward with speed ",self.CUR_SPEED)
    def move_backward(self,speed=0):
        if self.CUR_SPEED>-self.MAX_SPEED:
            self.CUR_SPEED-=1
        print("car moving backward with speed:",self.CUR_SPEED)
    def turn_right(self):
        print("car turnning right")
    def turn_left(self):
        print("car turnning left")

    def car_break(self):
        if(self.CUR_SPEED!=0):
            self.CUR_SPEED=self.CUR_SPEED+(1 if self.CUR_SPEED<0 else -1)
            print('Breaking... %d'%self.CUR_SPEED)
        else:
            print("Car already stopped.")
        return 
    def X_pressed(self):
        print("X pressed!")
        self.CUR_SPEED=0
        print('Speed set to 0')
    def fetch_current_coor(self):
        cy=(ADC.read(0)-self.oy)
        if cy>0:
            cy/=float(self.ground['y'][1]-self.oy)
        else:
            cy/=float(self.oy-self.ground['y'][0])
        
        cx=(ADC.read(1)-self.ox)
        if cx>0:
            cx/=float(self.ground['x'][1]-self.ox)
        else:
            cx/=float(self.ox-self.ground['x'][0])

        cp=ADC.read(2)/float(self.ground['p'][1])
        if abs(cx)<self.ground_threshold:
            cx=0.
        elif abs(cx-1)<self.ground_threshold:
            cx=1.
        if abs(cy)<self.ground_threshold:
            cy=0.
        elif abs(cy-1)<self.ground_threshold:
            cy=1.

        if abs(cp)<self.ground_threshold:
            cp=0.
        elif abs(cp-1)<self.ground_threshold:
            cp=1.
        return cy,cx,cp 
    def loop_coor(self):
        while(True):
            print(ADC.read(0),ADC.read(1),ADC.read(2),self.fetch_current_coor())
    def loop(self):
        while(True):
            y,x,p=self.fetch_current_coor()
            if y==0. and x==0. and self.CUR_SPEED!=0:
                self.car_break()
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
            self.destroy()
    
if __name__=='__main__':
    CC=CarController()
    CC.listen()
