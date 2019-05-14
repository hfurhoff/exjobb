from dto.pose import Pose
from dto.searchareadto import SearchareaDTO
from dto.vehicledto import VehicleDTO
from dto.point import Point
from dto.sensor import Sensor

class Settings():
	vehicle = None
	strategy = None
	area = None
	waypointPath = None
	lookaheadDepth = None
	
	def __init__(self, height, width, course, strategy, waypointPath, lookaheadDepth, gridsize, maxSpeed, targetx, targety, sensorRad, turningRadius):
		self.area = SearchareaDTO([height, width, gridsize, targetx, targety])
		self.strategy = strategy
		
		pos = self.initialPosition(height, width, course)
		pose = Pose(course, pos)
		currentSpeed = maxSpeed
		sensor = None
		if strategy == 'spiral.py':
			sensor = Sensor(sensorRad, True)
		else:
			sensor = Sensor(sensorRad, False)
		self.vehicle = VehicleDTO([pose, maxSpeed, currentSpeed, turningRadius, sensor])

		self.waypointPath = waypointPath
		self.lookaheadDepth = lookaheadDepth
	
	def initialPosition(self, height, width, course):
		bigDia = max([height, width])
		halfSideLength = 0.6 * bigDia
		
		entranceAngle = (course - 180) % 360
		if entranceAngle > 45 and entranceAngle <= 135:
			entranceX = halfSideLength
			entranceY = halfSideLength * (entranceAngle - 90) / 45
		elif entranceAngle > 135 and entranceAngle <= 225:
			entranceX = halfSideLength * (180 - entranceAngle) / 45
			entranceY = halfSideLength
		elif entranceAngle > 225 and entranceAngle <= 315:
			entranceX = -halfSideLength
			entranceY = halfSideLength * (270 - entranceAngle) / 45
		else: 
			if entranceAngle > 315:
				entranceX = halfSideLength * (entranceAngle - 360) / 45
			else:
				entranceX = halfSideLength * entranceAngle / 45
			entranceY = -halfSideLength
			
		return Point(entranceX, entranceY)
		
		
	def getVehicle(self):
		return self.vehicle
		
	def getStrategy(self):
		return self.strategy
	
	def getArea(self):
		return self.area
		
	def getLookaheadDepth(self):
		return self.lookaheadDepth
		
	def getSensor(self):
		return self.vehicle.getSensor()