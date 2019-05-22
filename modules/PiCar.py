from HardWare.BackWheel import Back_Wheels
from HardWare.FrontWheel import Front_Wheels
from HardWare.Ultrasonic import Ultrasonic_Avoidance
from HardWare.PCF8591_Car import PCF8591
import time
class PiCar:
    def __init__(self,debug=False):
        self.front_wheels=Front_Wheels(debug=debug)
        self.back_wheels=Back_Wheels(debug=debug)
        self.front_wheels.ready()
        self.UA=Ultrasonic_Avoidance(channel=20)
        self.LD=PCF8591(0x48)
    def move_forward(self):
        self.back_wheels.calibration()
    def stop_after(self,seconds):
        time.sleep(seconds)
        self.back_wheels.cali_ok()
#     def test_light(self):
#         self.LF.read
    def test_wheels(self):
        DELAY=3
        self.move_forward()
        self.stop_after(DELAY)
        self.back_wheels.backward()
        for i in range(0, 100):
            self.back_wheels.speed = i
            print("Backward, speed =", i)
            time.sleep(DELAY)
        for i in range(100, 0, -1):
            self.back_wheels.speed = i
            print("Backward, speed =", i)
            time.sleep(DELAY)

if __name__ == '__main__':
    car=PiCar()
    car.test_wheels()