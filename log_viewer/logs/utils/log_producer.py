import json
from confluent_kafka import Producer
import socket
topic='app_logs'
class ProducerLogCreated:
    def __init__(self) -> None:        
        conf = {'bootstrap.servers': "localhost:9092",'client.id': socket.gethostname()}
        self.producer = Producer(conf)

    # This method will be called inside view for sending Kafka message
    def publish(self,method, body):
        print('Inside UserService: Sending to Kafka: ')
        print(body)
        self.producer.produce(topic, key="key.logs.created", value=json.dumps(body))