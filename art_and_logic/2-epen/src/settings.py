# Load all env variables from .env file

import os

from dotenv import load_dotenv
from pathlib import Path  

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# General constants
LOG_LEVEL = os.getenv('LOG_LEVEL')
LOG_FORMAT = os.getenv('LOG_FORMAT')
BOUNDARY_LIMIT_ENC = os.getenv('BOUNDARY_LIMIT_ENC')
BOUNDARY_LIMIT_DEC = os.getenv('BOUNDARY_LIMIT_DEC')
INPUT_STREAM_FILE = os.getenv('INPUT_STREAM_FILE')