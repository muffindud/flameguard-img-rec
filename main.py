from pika import BlockingConnection, ConnectionParameters
from dotenv import load_dotenv

from src.model import scan_image

exchange = "img_rec"
send_to = "receive"
received_from = "send"


def callback(ch, method, properties, body):
    img_path = body.decode()
    result = scan_image(img_path)
    response = f"result {result[0]} {result[1]}"
    channel.basic_publish(exchange=exchange, routing_key=send_to, body=response)


config = load_dotenv()
connection = BlockingConnection(ConnectionParameters(host="localhost"))
channel = connection.channel()
channel.exchange_declare(exchange=exchange, exchange_type="direct")
result = channel.queue_declare(queue="", exclusive=True)
callback_queue = result.method.queue
channel.queue_bind(exchange=exchange, queue=callback_queue, routing_key=received_from)
channel.basic_consume(queue=callback_queue, on_message_callback=callback, auto_ack=True)


def main():
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        connection.close()
        exit(0)
