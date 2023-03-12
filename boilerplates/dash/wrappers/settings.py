# Load all env variables from .env file

import os

from dotenv import load_dotenv
from pathlib import Path  

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# General constants
PORT = os.getenv('PORT')