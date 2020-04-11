'''
This will be built upon in the future
	author: Jack Donofrio
'''
class Course:
	def __init__(self, name, grade):
		self.__name = name
		self.__grade = grade

	def get_grade(self):
		return self.__grade

	def get_name(self):
		return self.__name