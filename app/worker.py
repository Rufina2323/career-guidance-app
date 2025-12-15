import json
import uuid
import pika
from messaging.rabbitmq import get_connection
from services.ml_model_service import MLModelService


def callback(ch, method, properties, body):
    data = json.loads(body)
    ml_model_service = MLModelService()

    try:
        prediction = ml_model_service.predict(
            uuid.UUID(data["ml_model_id"]),
            uuid.UUID(data["response_data_id"]),
            data["payload"],
        )
        print(prediction, flush=True)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print("Error:", e)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def main():
    connection = get_connection()
    channel = connection.channel()

    channel.queue_declare(queue="ml_requests", durable=True)

    channel.basic_qos(prefetch_count=1)  # fair dispatch

    channel.basic_consume(queue="ml_requests", on_message_callback=callback)
    print("Worker started")
    channel.start_consuming()


if __name__ == "__main__":
    main()
