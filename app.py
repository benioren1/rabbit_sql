from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient

from dataa.db_connection import check_db_connection, get_collection_Shipments, get_collection_purchases
from blu_prints.users_routes import my_blueprint
from blu_prints.inventory_routes import bp_inventory
from models.inventory import Inventory, Base

app = Flask(__name__)

# חיבור לפוסטגרס
DATABASE_URL = "postgresql://postgres:1234@localhost/rabbitdata"
engine = create_engine(DATABASE_URL)

# יצירת ה-Session
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

# חיבור למונגוDB
app.config['MONGO_URI'] = 'mongodb://localhost:27017/rabbit_data'
mongo_client = MongoClient(app.config['MONGO_URI'])
db = mongo_client['rabbit_data']


# פונקציה לבדיקת חיבור לדאטה-בייס PostgreSQL
def check_db_connection():
    try:
        with engine.connect() as conn:
            print("Connection to database is successful.")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)


# הגדרת כל הפונקציות וה-Blueprints
app.register_blueprint(my_blueprint)
app.register_blueprint(bp_inventory)

# חיבור למונגוDB ובדיקת החיבור לדאטה-בייס PostgreSQL
with app.app_context():
    check_db_connection()

# יצירת כל הטבלאות אם הן לא קיימות
# אם תרצה ליצור את הטבלאות אוטומטית, תוכל להפעיל את השורה הבאה:
Base.metadata.create_all(bind=engine)

# הפעלת השרת
if __name__ == '__main__':
    # חיבור לקולקשנים של MongoDB
    collection_Shipments = get_collection_Shipments()
    collection_purchases = get_collection_purchases()

    # הפעלת השרת
    app.run(debug=True)
