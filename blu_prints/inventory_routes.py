from flask import Blueprint, request, jsonify

from dataa.db_connection import  session
from models.inventory import Inventory

bp_inventory = Blueprint('inventory', __name__)


@bp_inventory.route('/inventory', methods=['POST'])
def add_inventory():
    data = request.get_json()
    new_item = Inventory(**data)
    session.add(new_item)
    session.commit()
    return jsonify(new_item.to_dict()), 201