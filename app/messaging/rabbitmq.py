import pika
import os
import json

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")


def get_connection():
    return pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))


def publish(queue: str, message: dict):
    connection = get_connection()
    channel = connection.channel()

    channel.queue_declare(queue=queue, durable=True)

    channel.basic_publish(
        exchange="",
        routing_key=queue,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2  # persistent
        ),
    )

    connection.close()
