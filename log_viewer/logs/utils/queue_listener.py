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
conf = {'bootstrap.servers': "localhost:9092",
        'auto.offset.reset': 'smallest',
        'group.id': "logs_group",
        # 'enable.auto.commit': True,
}
#Topic 
#improvement make this as configuration variable
topic='app_logs'


class LogsCreatedListener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # Create consumer
        self.consumer = Consumer(conf)
   
        
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
                    continue
                #Handle Error
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        print('%% %s [%d] reached end at offset %d\n' %(msg.topic(), msg.partition(), msg.offset()))
                    # End of partition event
                        # sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                        #              (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    print("error")
                    raise KafkaException(msg.error())
                else:
                    #Handle Message
                    print('---------> Got message creating log.....')
                    log_data = json.loads(msg.value().decode('utf-8'))
                    #In Real world, write email sending logic here
                    log_entry = LogData.objects.create(
                        level=log_data["level"],
                        message=log_data["message"],
                        resourceId=log_data["resourceId"],
                        timestamp=datetime.strptime(log_data["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc),
                        traceId=log_data["traceId"],
                        spanId=log_data["spanId"],
                        commit=log_data["commit"],
                        parentResourceId=log_data["metadata"].get("parentResourceId")
                    )
                    log_entry.save()
                    print(log_data)
        finally:
        # Close down consumer to commit final offsets.
            self.consumer.close()
    
   