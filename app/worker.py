import json
import uuid
import pika
from messaging.rabbitmq import get_connection
from models.ml_request import Status
from services.ml_model_service import MLModelService
from services.ml_request_service import MLRequestService


def callback(ch, method, properties, body):
    data = json.loads(body)
    ml_model_service = MLModelService()
    ml_request_service = MLRequestService()

    try:
        ml_request_service.change_ml_request_status(
            ml_request_id=data["request_id"], ml_request_status=Status.RUNNING
        )
        prediction = ml_model_service.predict(
            uuid.UUID(data["ml_model_id"]),
            uuid.UUID(data["response_data_id"]),
            data["payload"],
        )
        ml_request_service.change_ml_request_status(
            ml_request_id=data["request_id"], ml_request_status=Status.COMPLETED
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        ml_request_service.change_ml_request_status(
            ml_request_id=data["request_id"], ml_request_status=Status.FAILED
        )
        ml_request_service.fail_ml_request(ml_request_id=data["request_id"])
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
