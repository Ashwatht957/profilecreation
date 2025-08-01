import os
from dotenv import load_dotenv
from pyairtable import Table

# Load environment variables from .env file
load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")

# Initialize the Airtable Table
def get_table():
    return Table(AIRTABLE_API_KEY, BASE_ID, TABLE_NAME)

# Fetch a single candidate record by name
def get_record_by_name(name):
    table = get_table()
    formula = f"{{Candidate Name}} = '{name}'"
    records = table.all(formula=formula)
    return records[0] if records else None

# Fetch all candidate records
def get_all_candidates():
    table = get_table()
    return table.all()
