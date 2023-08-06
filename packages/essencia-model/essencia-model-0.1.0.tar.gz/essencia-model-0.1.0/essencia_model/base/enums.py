from enum import Enum


class BaseEnum(Enum):
	def __str__(self):
		return self.value
	
	@property
	def json(self):
		return self.name
	
	@classmethod
	def is_enum(cls):
		return True


class Gender(BaseEnum):
	M = 'Masculino'
	F = 'Feminino'
	
	