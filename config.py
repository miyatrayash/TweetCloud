import os
from dotenv import load_dotenv

# Load ENV variables
load_dotenv()

class Config(object):
    TW_BEARER_TOKEN = os.environ.get('TW_BEARER_TOKEN')
    TW_API_KEY = os.environ.get('TW_API_KEY')
    TW_API_SECRET_KEY = os.environ.get('TW_API_SECRET_KEY')
    TW_BASE_URL = os.environ.get('TW_BASE_URL')
    REPO_URL = os.environ.get('REPO_URL')
