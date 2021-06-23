import psycopg2
from psycopg2 import OperationalError
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
try:
    db_connection = psycopg2.connect(
        database=os.getenv("DATABASE"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST"),
        port=os.getenv("PORT")
    )
except OperationalError as err:
    print(f"{err}")
