import datetime
import os
import uuid

import pika
import json

from pika import PlainCredentials
from tqdm import tqdm


class LSMSClient(object):

    def __init__(self, username=None, password=None):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('scheduler.xfact.net',
                                                                       5672,
                                                                       "lm",
                                                                       credentials=PlainCredentials(username=username or os.getenv("AMQ_USERNAME", ""),
                                                                                                    password=password or os.getenv("AMQ_PASSWORD","")),
                                                                       heartbeat=20000))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n, tokenizer_kwargs=None, generate_kwargs=None):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='lm',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
                expiration='20000',
            ),

            body=json.dumps({
                "text": n,
                "tokenizer_kwargs": tokenizer_kwargs or {},
                "generate_kwargs": generate_kwargs or {}
            }))

        self.connection.process_data_events(time_limit=20)

        if self.response:
            return json.loads(self.response.decode('utf-8'))
        else:
            return None


if __name__ == "__main__":
    client = LSMSClient()

    while tqdm(True):
        print(client.call("Tell me about X", generate_kwargs={"max_new_tokens":10,
                                                                     "do_sample": False,
                                                                     "num_return_sequences":1}))

