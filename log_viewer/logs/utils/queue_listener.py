import json
import sys 
import threading
from confluent_kafka import Consumer
from confluent_kafka import KafkaError
from confluent_kafka import KafkaException
from datetime import datetime
from logs.models import LogData
from django.utils import timezone


#We want to run thread in an infinite loop
running=True
conf = {'bootstrap.servers': 'localhost:9092',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False,
        'group.id': "logs_group",
        
}
#Topic 
#improvement make this as configuration variable
topic='app_logs'


class LogsCreatedListener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # Create consumer
        self.consumer = Consumer(conf)
        self.batch_size = 100 # increase batch size to 100 if request volume is high
        self.messages_batch = []
   
        
    def run(self):
        print ('Inside LogListenerService :  Created Listener ')
        try:
            #Subcribe to topic
            self.consumer.subscribe([topic])
            while running:
                #Poll for message
                msg = self.consumer.poll(timeout=1.0)
                if msg is None: 
                    print("No message found")
                    # if there is anything in batch
                    self.insert_batch()
                    continue
                #Handle Error
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        print('%% %s [%d] reached end at offset %d\n' %(msg.topic(), msg.partition(), msg.offset()))
                        self.insert_batch()
                    print("error %s" % msg.error())
                    raise KafkaException(msg.error())
                else:
                    #Handle Message
                    print('---------> Got message creating log.....')
                    log_data = json.loads(msg.value().decode('utf-8'))
                    log_entry = LogData(
                        level=log_data["level"],
                        message=log_data["message"],
                        resourceId=log_data["resourceId"],
                        timestamp=datetime.strptime(log_data["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc),
                        traceId=log_data["traceId"],
                        spanId=log_data["spanId"],
                        commit=log_data["commit"],
                        parentResourceId=log_data["metadata"].get("parentResourceId")
                    )
                    self.messages_batch.append(log_entry)
                    # Insert in batches
                    if len(self.messages_batch) >= self.batch_size:
                        self.insert_batch()
        finally:
        # Close down consumer to commit final offsets.
            self.insert_batch()
            self.consumer.close()
    
    def insert_batch(self):
        if self.messages_batch:
            LogData.objects.bulk_create(self.messages_batch)
            self.messages_batch = []
            self.consumer.commit(asynchronous=False)
            print("logs inserted successfully.")

        
   