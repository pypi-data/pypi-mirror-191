import json
import os
import anyio
from typing import Optional, Union, ClassVar
from datetime import date
from pydantic import BaseModel, validator
from pydantic.fields import Field
from deta import Deta

from .enums import Gender
from essencia_model import context
from essencia_model.config import config, templates


def remove_extra_white_spaces(string: str) -> str:
	return ' '.join([item.strip() for item in string.split()])


def capitalize_name(string: str) -> str:
	return ' '.join([item.strip().capitalize() for item in string.split()])


def only_numbers(string: str) -> str:
	return ''.join([item for item in string.strip() if item.isdigit()])


class Model(BaseModel):
	key: Optional[str] = None
	context_tables: ClassVar[list[str]] = []
	
	class Config:
		anystr_strip_whitespace = True
		extra = 'ignore'
		
	@classmethod
	def context_data(cls):
		return templates.env.globals[cls.__name__]
	
	@classmethod
	def context_instances(cls):
		return [cls(**item) for item in cls.context_data().values()]
	
	@classmethod
	async def setup_context(cls):
		return await context.setup_context([*cls.context_tables, cls.__name__])

	@classmethod
	def field_type(cls, field_name: str):
		return cls.__annotations__[field_name]
		
	@classmethod
	def parse_enum(cls, field_name: str, value: str):
		if isinstance(value, str):
			try:
				value = cls.field_type(field_name)[value]
			except BaseException as e:
				print(e)
				value = cls.field_type(field_name)(value)
		assert value in cls.field_type(field_name).__members__.values()
		return value
	
	def dict(self, *args, **kwargs):
		kwargs['exclude_none'] = {'key'}
		data = super().dict(*args, **kwargs)
		return data
		
	def json(self, *args, **kwargs):
		kwargs['exclude_none'] = {'key'}
		data = json.loads(super().json(*args, **kwargs))
		for item in data.copy():
			try:
				if self.field_type(item).is_enum():
					data[item] = getattr(self, item).name
			except AttributeError:
				pass
		return json.dumps(data)
	

class Person(Model):
	fname: str
	lname: str
	bdate: date
	gender: Gender = Field()
	cpf: Optional[str]
	transgender: bool = False
	non_binary: bool = False
	name: str = ''
	
	_validate_fname = validator('fname', pre=True, allow_reuse=True)(capitalize_name)
	_validate_lname = validator('lname', pre=True, allow_reuse=True)(capitalize_name)

	@validator('gender', pre=True)
	def validate_gender(cls, v):
		return cls.parse_enum('gender', v)
	
	@validator('cpf', pre=True, always=True)
	def validate_cpf(cls, v):
		if v:
			v = only_numbers(v)
			print(v)
			assert len(v) == 11, 'O CPF deve conter 11 dígitos'
			return f'{v[:3]}.{v[3:6]}.{v[6:9]}-{v[9:]}'
		return v


class BaseProfile(Model):
	person_key: str
	phone: str = None
	email: str = None
	address: str = None
	city: str = None
	notes: str = None
	search: str = None
	key: str = None
	context_tables: ClassVar[list[str]] = ['Person']
	
	def __str__(self):
		return str(self.person)
	
	@property
	def person(self):
		return Person(**templates.env.globals['Person'][self.person_key])

	
class Doctor(BaseProfile):
	pass
	
	