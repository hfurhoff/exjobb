class Util():

	def __init__(self):
		pass

	@staticmethod
	def unwrap(diff):
		if diff == 0:
			return diff
		sign = diff / abs(diff)
		if abs(diff) > 180:
			if sign < 0:
				diff = diff + 360
			else:
				diff = diff - 360
		return diff