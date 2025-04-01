import os
from dotenv import load_dotenv

# load the .env file
load_dotenv()

class Config:
# default to localhost
    BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
    
# Creates a singleton instance:
settings = Config()