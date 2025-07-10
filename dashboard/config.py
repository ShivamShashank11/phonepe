from sqlalchemy import create_engine
from urllib.parse import quote_plus

def get_engine():
    password = quote_plus("Nicky@123")
    return create_engine(f"mysql+mysqlconnector://root:{password}@localhost:3306/phonepe_insights")
