from sqlalchemy import create_engine

def get_engine():
    return create_engine("mysql+mysqlconnector://root:Nicky%40123@localhost:3306/phonepe_insights")

engine = get_engine()

with engine.connect() as conn:
    result = conn.execute("SELECT DATABASE();")
    print("✅ Connected to:", result.fetchone()[0])
