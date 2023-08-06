# encoding: utf-8
# Date: 2023/2/13 10:00

__author__ = 'easy'

from kafka import KafkaProducer, KafkaConsumer
from kafka.structs import TopicPartition
import json


class KafkaProducerUtils(object):
    def __init__(self, **configs):
        self.producer = KafkaProducer(
            **configs
        )

    def send(self, topic, msg):
        self.producer.send(topic, json.dumps(msg).encode("utf-8"))

    def flush(self):
        self.producer.flush()


class KafkaConsumeUtils(object):
    def __init__(self, *topic, **config):
        self.consumer = KafkaConsumer(*topic, **config)

    def get(self):
        for msg in self.consumer:
            print("msg->:", msg)

