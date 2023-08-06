# encoding: utf-8
# Date: 2023/2/13 13:23

__author__ = 'easy'
from easy.kafka_utils import KafkaProducerUtils, KafkaConsumeUtils


def test_producer():
    config = dict(
        bootstrap_servers=['172.16.200.138:9092'],
        security_protocol="SASL_PLAINTEXT",
        sasl_mechanism="PLAIN",
        sasl_plain_username="tip",
        sasl_plain_password="@70#*WfaAS?>S3*7"
    )
    producer = KafkaProducerUtils(**config)
    topic = "csdn"
    producer.send(topic, "nihao呀")
    producer.send(topic, "nihao呀丫丫")
    producer.flush()


def test_consume():
    config = dict(
        bootstrap_servers=['172.16.200.138:9092'],
        group_id='test-consumer-group',
        auto_offset_reset='latest',
        enable_auto_commit=False,
        security_protocol="SASL_PLAINTEXT",
        sasl_mechanism="PLAIN",
        sasl_plain_username="tip",
        sasl_plain_password="@70#*WfaAS?>S3*7"
    )
    topic = ["csdn"]
    consume = KafkaConsumeUtils(*topic, **config)
    consume.get()


if __name__ == '__main__':
    test_consume()



