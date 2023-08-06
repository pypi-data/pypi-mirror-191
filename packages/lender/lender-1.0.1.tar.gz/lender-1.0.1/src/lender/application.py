import os
import tornado.ioloop
import tornado.web


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

settings = dict(
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "statics")
    )

def Serving(port, handlers):
    handlers.append((r"/", IndexHandler))
    for h in handlers:
        print(h[0])
    
    application = tornado.web.Application(handlers, **settings)
    application.listen(port)
    # 二级域名
    # application.add_handlers(r"www\.myhost\.com", [
    #     (r"/article/([0-9]+)", ArticleHandler),
    # ])
    tornado.ioloop.IOLoop.current().start()