from dotenv import load_dotenv
from os import getenv, path

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(dotenv_path=path.join(BASE_DIR, ".env"))

# Now we will load the constants
DB_URI = getenv("DB_URI").strip()
