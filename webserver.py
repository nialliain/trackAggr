import tornado.ioloop
import tornado.web
import tornado.websocket
import MySQLdb
import json
from config import setupChannel, topicName

db=MySQLdb.connect(user='niall', db="tracker", host='localhost')
c=db.cursor()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json')
        c.execute('select * from points')
        self.write( json.dumps( [{'lat':'{0:f}'.format(r[1]),'lon':'{0:f}'.format(r[2]),'at':str(r[3])} for r in c.fetchall()], indent=2))

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        channel = setupChannel()
        result = channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=topicName, queue=queue_name, routing_key='#')

        def callback(ch, method, properties, body):
            body = body.decode("utf-8")
            self.write_message(body)

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/updates", EchoWebSocket),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()