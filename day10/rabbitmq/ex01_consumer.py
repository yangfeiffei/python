#!/usr/bin/python3
#_*_coding:utf-8_*_
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

for method_frame, properties, body in channel.consume('test'):

    # Display the message parts and ack the message
    print(method_frame, properties, body)
    channel.basic_ack(method_frame.delivery_tag)

    # Escape out of the loop after 10 messages
    if method_frame.delivery_tag == 10:
        break

# Cancel the consumer and return any pending messages
requeued_messages = channel.cancel()
print('Requeued %i messages' % requeued_messages)
connection.close()