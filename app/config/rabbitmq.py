import os
from dotenv import load_dotenv


load_dotenv()

RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")

assert RABBITMQ_QUEUE is not None
