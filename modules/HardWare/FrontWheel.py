import os,sys
sys.path.append('~/Lab/Zeusy')
from fileDB import fileDB
from Servo import Servo

class Front_Wheels(object):
	''' Front wheels control class '''
	FRONT_WHEEL_CHANNEL = 0
	def __init__(self, debug=False, db="config", bus_number=1, channel=FRONT_WHEEL_CHANNEL):
		''' setup channels and basic stuff '''
		self.db = fileDB(db=db)
		self.channel = channel
		self.straight_angle = 90
		self.turning_max = 45
		self.DEBUG_INFO = 'DEBUG "front_wheels.py":'
		# self.turning_offset = int(self.db.get('turning_offset', default_value=0))
		self.turning_offset = 25
		self.wheel = Servo(self.channel, bus_number=bus_number, offset=self.turning_offset)
		self.DEBUG = debug
		self.set_turning_max(45)
		self.min_angle=30
		self.max_angle=150.
		if self.DEBUG:
			print(self.DEBUG_INFO, 'Front wheel PWM channel:', self.channel)
			print(self.DEBUG_INFO, 'Front wheel offset value:', self.turning_offset)
		self.angle = {"left":self.min_angle, "straight":self.straight_angle, "right":self.max_angle}
		if self.DEBUG:
			print(self.DEBUG_INFO, 'left angle: %s, straight angle: %s, right angle: %s' % (self.angle["left"], self.angle["straight"], self.angle["right"]))
		# self.calibration()
		# self.set_turning_offset()
	def turn_left(self):
		''' Turn the front wheels left '''
		if self.DEBUG:
			print(self.DEBUG_INFO, "Turn left")
		self.wheel.write(self.angle["left"])

	def turn_straight(self):
		''' Turn the front wheels back straight '''
		if self.DEBUG:
			print(self.DEBUG_INFO, "Turn straight")
		self.wheel.write(self.angle["straight"])

	def turn_right(self):
		''' Turn the front wheels right '''
		if self.DEBUG:
			print(self.DEBUG_INFO, "Turn right")
		self.wheel.write(self.angle["right"])

	def turn(self, angle):
		''' Turn the front wheels to the giving angle '''
		if self.DEBUG:
			print(self.DEBUG_INFO, "Turn to", angle)
		if angle < self.angle["left"]:
			angle = self.angle["left"]
		if angle > self.angle["right"]:
			angle = self.angle["right"]
		self.wheel.write(angle)
	
	def set_turning_max(self, angle):
		self.turning_max = angle
		self.min_angle = self.straight_angle - angle
		self.max_angle = self.straight_angle + angle
		self.angle = {"left":self.min_angle, "straight":self.straight_angle, "right":self.max_angle}


	def set_turning_offset(self, value):
		if not isinstance(value, int):
			raise TypeError('"turning_offset" must be "int"')
		self.turning_offset = value
		self.db.set('turning_offset', value)
		self.wheel.offset = value
		self.turn_straight()

	def set_debug(self, debug):
		''' Set if debug information shows '''
		if debug in (True, False):
			self.DEBUG = debug
		else:
			raise ValueError('debug must be "True" (Set debug on) or "False" (Set debug off), not "{0}"'.format(debug))
		if self.DEBUG:
			print(self.DEBUG_INFO, "Set debug on")
			print(self.DEBUG_INFO, "Set wheel debug on")
			self.wheel.debug = True
		else:
			print(self.DEBUG_INFO, "Set debug off")
			print(self.DEBUG_INFO, "Set wheel debug off")
			self.wheel.debug = False

	def ready(self):
		''' Get the front wheels to the ready position. '''
		if self.DEBUG:
			print(self.DEBUG_INFO, 'Turn to "Ready" position')
		self.wheel.offset = self.turning_offset
		self.turn_straight()

	def calibration(self):
		''' Get the front wheels to the calibration position. '''
		if self.DEBUG:
			print(self.DEBUG_INFO, 'Turn to "Calibration" position')
		self.turn_straight()
		self.cali_turning_offset = self.turning_offset

	def cali_left(self):
		''' Calibrate the wheels to left '''
		self.cali_turning_offset -= 1
		self.wheel.offset = self.cali_turning_offset
		self.turn_straight()

	def cali_right(self):
		''' Calibrate the wheels to right '''
		self.cali_turning_offset += 1
		self.wheel.offset = self.cali_turning_offset
		self.turn_straight()

	def cali_ok(self):
		''' Save the calibration value '''
		self.turning_offset = self.cali_turning_offset
		self.db.set('turning_offset', self.turning_offset)

	def test(self,chn=0):
		import time
		front_wheels = Front_Wheels(channel=chn)
		try:
			while True:
				print("turn_left")
				front_wheels.turn_left()
				time.sleep(1)
				print("turn_straight")
				front_wheels.turn_straight()
				time.sleep(1)
				print("turn_right")
				front_wheels.turn_right()
				time.sleep(1)
				print("turn_straight")
				front_wheels.turn_straight()
				time.sleep(1)
		except KeyboardInterrupt:
			front_wheels.turn_straight()
import time
if __name__ == '__main__':
	fw=Front_Wheels()
	# fw.ready()
	fw.wheel.write(fw.angle['straight'])
	time.sleep(3)
	for ang in xrange(-30,30,5):
		time.sleep(1)
		print(ang)
		fw.turn(fw.angle['straight']+ang)
	fw.wheel.write(fw.angle['straight'])