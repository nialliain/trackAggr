from config import setupChannel, topicName
import MySQLdb

db=MySQLdb.connect(user='niall', db="tracker", host='localhost')
c=db.cursor()

channel = setupChannel()
result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange=topicName, queue=queue_name, routing_key='#')
def callback(ch, method, properties, body):
    body = body.decode("utf-8")
    print(body)
    b = body.split(',')
    sql = "insert into points values ( '{}', {}, {}, '{}' ); commit;".format(b[2], b[0], b[1], b[3])
    print(sql)
    c.execute(sql)
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()