import json
class Information(object):
	def __init__(self, j):
		self.__dict__ = json.loads(j)