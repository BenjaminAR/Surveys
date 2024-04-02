from .settings import *
from decouple import config


ALLOWED_HOSTS = config('ALLOWED_HOSTS_PRD', cast=lambda v: [s.strip() for s in v.split(',')])

DEBUG = config('DEBUG_PRD', default=False, cast=bool)