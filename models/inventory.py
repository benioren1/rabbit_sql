from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

# יצירת בסיס למודלים
Base = declarative_base()


class Inventory(Base):
    __tablename__ = 'inventory'

    # עמודות הטבלה
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=True)
    price = Column(Float, nullable=False)

    # המרת המודל למילון
    def to_dict(self):
        return {
            'id': self.id,
            'item_name': self.item_name,
            'quantity': self.quantity,
            'price': self.price
        }