import os
import tornado.ioloop
import tornado.web
import tornado.websocket

opened_ws = []

class WebSocketAction(tornado.websocket.WebSocketHandler):
    def open(self):
        print "WebSocket opened"
        opened_ws.append(self)
        self.write_message("Connection ok")

    def on_close(self):
        opened_ws.remove(self)
        print "WebSocket closed"


class MessageHandler(tornado.web.RequestHandler):    
    def get(self, action_id):    
        print "Message = " + action_id
        for ws in opened_ws:
            ws.write_message(action_id)


if __name__ == "__main__":
    
    application = tornado.web.Application([
        (r"/msg/(.*)", MessageHandler),
        (r"/ws", WebSocketAction),
	])
    application.listen(8888)
    
    tornado.ioloop.IOLoop.instance().start()
