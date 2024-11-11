import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# הגדרת ה-Base
Base = declarative_base()

# הגדרת המידע להתחברות לדאטהבייס
DATABASE_URL = "postgresql://postgres:1234@localhost/rabbitdata"

# יצירת ה-Engine
engine = create_engine(DATABASE_URL)

# יצירת ה-Session
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()


def check_db_connection():
    try:
        conn = psycopg2.connect(
            dbname='rabbitdata',
            user='postgres',
            password='1234',
            host='localhost',
            port='5432'
        )
        conn.close()
        print("Connection to database is successful.")
    except psycopg2.OperationalError as e:
        print(f"Error: {e}")
        exit(1)

from pymongo import MongoClient
from confing_mongo import MONGO_URI, DB_NAME, COLLECTION_NAME_1, COLLECTION_NAME_2

def get_collection_Shipments():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME_1]
    return collection

def get_collection_purchases():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME_2]
    return collection

