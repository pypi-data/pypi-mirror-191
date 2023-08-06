import os.path

from starlette.config import Config
from starlette.templating import Jinja2Templates


config = Config(os.path.join(os.getcwd(), '.env'))

templates = Jinja2Templates(directory=os.path.join(os.getcwd(), 'templates'))