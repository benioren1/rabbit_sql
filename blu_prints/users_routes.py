from flask import Blueprint, request, jsonify

from dataa.db_connection import session
from rabbit.producer import publish_message
from models.users import User
from models.inventory import Inventory


# יצירת ה-Blueprint
my_blueprint = Blueprint('my_blueprint', __name__)

# מסלול רישום משתמש חדש
@my_blueprint.route('/signup', methods=['POST'])
def signup_route():
    data = request.get_json()  # קבלת נתוני JSON מהבקשה
    try:
        # יצירת משתמש חדש
        new_user = User(**data)
        session.add(new_user)
        session.commit()
        return jsonify(new_user.to_dict()), 201  # מחזירים את המידע של המשתמש החדש
    except Exception as e:
        session.rollback()  # אם קרתה שגיאה, מבצעים רולבק
        return jsonify({"error": str(e)}), 500

# מסלול רכישת מוצר
@my_blueprint.route('/buy', methods=['POST'])
def buy_route():
    data = request.get_json()  # קבלת נתוני JSON על הרכישה
    try:
        # חיפוש משתמש על פי אימייל
        user = session.query(User).filter_by(email=data['email']).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404  # אם המשתמש לא נמצא

        # חיפוש המוצר במלאי
        item = session.query(Inventory).filter_by(item_name=data['item']).first()
        if not item:
            return jsonify({'error': 'Item not found in inventory'}), 404

        # עדכון הכמות במלאי
        item.quantity -= data['quantity']
        session.commit()

        # שליחה ל-RabbitMQ אם צריך (אם יש צורך)
        publish_message(data['item'], f"{data['item']} {data['quantity']} {data['email']}")

        return jsonify({'message': 'Purchase successful'}), 200  # מחזיר הודעה שהרכישה הצליחה
    except Exception as e:
        session.rollback()  # אם קרתה שגיאה, מבצעים רולבק
        return jsonify({"error": str(e)}), 500