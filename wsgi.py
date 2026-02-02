import sys
import os

# Add your project directory to the sys.path
project_home = '/home/YOUR_USERNAME/My_Diary'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Load environment variables from .env file
from dotenv import load_dotenv
project_folder = os.path.expanduser(project_home)
load_dotenv(os.path.join(project_folder, '.env'))

# Import Flask app
from app import app as application
