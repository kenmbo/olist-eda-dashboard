import sqlite3
import pandas as pd
import sys
from src import queries

def get_connection(db_path="../data/olist.sqlite"):
    """
    Adjust the db_path depending on where you run the script from.
    """
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database '{db_path}': {e}")
        sys.exit(1)
