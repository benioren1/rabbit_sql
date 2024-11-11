import pika
import time


from dataa.db_connection import session
from models.inventory import Inventory


def add_data(data):
    new_data = data.split(' ')
    product_name = new_data[0]
    quantity_to_deduct = int(new_data[1])
    product = session.query(Inventory).filter_by(item_name=product_name).first()
    if product:
        if product.quantity >= quantity_to_deduct:
            product.quantity -= quantity_to_deduct
            session.commit()
            print(f"Updated {product_name} quantity to {product.quantity}")
        else:
            print(f"Not enough quantity for {product_name}. Available: {product.quantity}")
    else:
        print(f"{product_name} not found in inventory.")




def callback(ch, method, properties, body):
    message = body.decode()
    add_data(message)
    print(f" [x] Received {message}")
    delay_time = len(message) * 0.5
    time.sleep(delay_time)
    print("[x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# יצירת חיבור ל-RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


channel.exchange_declare(exchange='moshe', exchange_type='direct')


channel.queue_declare(queue='inventory')
channel.queue_declare(queue='email')
channel.queue_declare(queue='shipments')


channel.queue_bind(exchange='moshe', queue='inventory', routing_key='inventory')
channel.queue_bind(exchange='moshe', queue='email', routing_key='email')
channel.queue_bind(exchange='moshe', queue='shipments', routing_key='shipments')


channel.basic_consume(queue='inventory', on_message_callback=callback, auto_ack=False)
channel.basic_consume(queue='email', on_message_callback=callback, auto_ack=False)
channel.basic_consume(queue='shipments', on_message_callback=callback, auto_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
