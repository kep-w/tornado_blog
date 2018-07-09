from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_config_file

from blog.app.myapp import IndexHandler, LoginHandler, BlogHandler, RegisterHandler, CheckHandler, LoginModule, \
    BlogModule, RegisterModule, MyApplication, PublishHandler

define('port', type=int, default=8888)
parse_config_file('../config/config')


app = MyApplication(hs=[('/', IndexHandler),
                        ('/login', LoginHandler),
                        ('/blog', BlogHandler),
                        ('/register', RegisterHandler),
                        ('/check', CheckHandler),
                        ('/publish', PublishHandler)],
                    tp='mytemplates',  # 模板路径,相对路径
                    sp='mystatics',  # 静态文件
                    um={'loginmodule': LoginModule,
                        'blogmodule': BlogModule,
                        'registermodule': RegisterModule})

server = HTTPServer(app)
server.listen(options.port)
IOLoop.current().start()

