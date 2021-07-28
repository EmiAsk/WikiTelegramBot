import os

import dotenv


dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
TOKEN = os.getenv('TOKEN')
ADMINS_ID = [747448837, 1804671709]
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'db')