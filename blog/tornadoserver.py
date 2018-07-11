import tornado.netutil
import tornado.process

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
# 创建多线程解决单线程问题
sockets = tornado.netutil.bind_sockets(options.port)
tornado.process.fork_processes(4)
server = HTTPServer(app)
server.add_sockets(sockets)
IOLoop.instance().start()
