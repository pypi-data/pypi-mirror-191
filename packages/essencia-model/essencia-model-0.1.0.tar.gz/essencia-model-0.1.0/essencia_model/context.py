import json
import os
import functools
import anyio
from contextvars import copy_context, ContextVar
from typing import Optional, NamedTuple, Union, ClassVar
from datetime import date, datetime, timedelta, timezone
from pydantic import BaseModel, validator, validate_arguments
from pydantic.fields import Field
from collections import ChainMap


from .database import get_list_by_table
from .config import templates

context = copy_context()

PersonVar = ContextVar('PersonVar', default=dict())
DoctorVar = ContextVar('DoctorVar', default=dict())
TherapistVar = ContextVar('TherapistVar', default=dict())
EmployeeVar = ContextVar('EmployeeVar', default=dict())
ServiceVar = ContextVar('ServiceVar', default=dict())
FacilityVar = ContextVar('FacilityVar', default=dict())

ContextData = ChainMap(
		{'Person': {'var': PersonVar, 'data': dict()}},
		{'Doctor': {'var': DoctorVar, 'data': dict()}},
		{'Therapist': {'var': TherapistVar, 'data': dict()}},
		{'Employee': {'var': EmployeeVar, 'data': dict()}},
		{'Service': {'var': ServiceVar, 'data': dict()}},
		{'Facility': {'var': FacilityVar, 'data': dict()}},
)


async def setup_context(table_list: list[str]):
	def set_context():
		nonlocal table
		ContextData[table]['var'].set(ContextData[table]['data'])
		templates.env.globals[table] = ContextData[table]['data']
	
	async def get_context_data():
		nonlocal table
		ContextData[table]['data'] = {item['key']: item for item in await get_list_by_table(table)}
		context.run(set_context)
	
	async with anyio.create_task_group() as tasks:
		for table in table_list:
			tasks.start_soon(get_context_data)


