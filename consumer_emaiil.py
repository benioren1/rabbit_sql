import pika
import time


from dataa.db_connection import session
from models.inventory import Inventory







def callback(ch, method, properties, body):
    message = body.decode()

    print(f" [x] Received {message}")
    delay_time = len(message) * 0.5
    time.sleep(delay_time)
    print("[x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# יצירת חיבור ל-RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


channel.exchange_declare(exchange='moshe', exchange_type='direct')

channel.queue_declare(queue='email')

channel.queue_bind(exchange='moshe', queue='email', routing_key='email')

channel.basic_consume(queue='email', on_message_callback=callback, auto_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
