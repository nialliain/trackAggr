topicName = 'points'

def setupChannel():
    import pika
    import config
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange=config.topicName, exchange_type='topic')
    return channel