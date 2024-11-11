import pika
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='moshe', exchange_type='direct')


channel.queue_declare(queue='inventory')
channel.queue_declare(queue='email')
channel.queue_declare(queue='shipments')

channel.queue_bind(exchange='moshe', queue='inventory', routing_key='inventory')
channel.queue_bind(exchange='moshe', queue='email', routing_key='email')
channel.queue_bind(exchange='moshe', queue='shipments', routing_key='shipments')

def publish_message(product_type, data):
    # product_type = product_type['item']
    routing_keys = {
        'Shoes': ['inventory', 'email', 'shipments'],
        'Shirt': ['inventory', 'email', 'shipments'],
        'Coupon': ['email'],
        'Travel Ticket': ['email'],
    }

    if product_type not in routing_keys:
        print(f"Product type '{product_type}' not recognized!")
        return

    # הוספת הודעות לכל routing_key
    for routing_key in routing_keys[product_type]:
        channel.basic_publish(
            exchange='moshe',
            routing_key=routing_key,
            body=data
        )
        print(f'[x] Sent "{data}" to routing key "{routing_key}"')

