import os
import time
from tornado.web import Application, RequestHandler, UIModule

from blog.util.dbutil import DBUtil
from blog.util.mysession import Session
from blog.util.myutil import mymd5


class MyApplication(Application):
    def __init__(self, hs, tp, sp, um):
        super().__init__(handlers=hs, template_path=tp, static_path=sp, ui_modules=um)
        self.dbutil = DBUtil()


class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        r = ''
        msg = self.get_query_argument('msg', None)
        if msg:
            r = '用户名或密码错误'
        s = Session(self)
        if s['islogin']:
            self.redirect('/blog')
        else:
            self.render('login.html', result=r)

    def post(self, *args, **kwargs):
        pass


class LoginHandler(RequestHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        uname = self.get_body_argument('uname')
        upwd = self.get_body_argument('upwd')
        upwd = mymd5(upwd)
        if self.application.dbutil.loginSuccess(uname, upwd):
            s = Session(self)
            s['islogin'] = True
            s['uname'] = uname
            # 跳转到主页
            self.redirect('/blog?uname=' + uname)
        else:
            # 跳转回登录页面,并传递错误信息
            self.redirect('/?msg=msg')


class BlogHandler(RequestHandler):
    def get(self, *args, **kwargs):
        s = Session(self)
        if s['islogin']:
            self.render('blog.html')
        else:
            self.redirect('/')

    def post(self, *args, **kwargs):
        pass


class RegisterHandler(RequestHandler):
    def get(self, *args, **kwargs):
        s = Session(self)
        if s['islogin']:
            self.redirect('/blog')
        else:
            self.render('register.html')

    def post(self, *args, **kwargs):
        uname = self.get_body_argument('uname', None)
        upwd = self.get_body_argument('upwd', None)
        city = self.get_body_argument('city', None)
        if uname and upwd and city:
            avatar = None
            if self.request.files:
                f = self.request.files['avatar'][0]
                body = f['body']
                fname = str(time.time()) + f['filename']
                with open('mystatics/images/%s' % fname, 'wb') as writer:
                    writer.write(body)
                avatar = fname
            upwd = mymd5(upwd)
            try:
                self.application.dbutil.registSave(uname, upwd, avatar, city)
            except Exception as e:
                if avatar:
                    os.remove('mystatics/images/%s' % avatar)
                err = str(e)
                self.redirect('/register?msg=' + err)
            else:
                self.redirect('/')
        else:
            self.redirect('/register?msg=empty')


class CheckHandler(RequestHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        type = self.get_body_argument('type',None)
        name = self.get_body_argument('uname', None)
        if type == 'register':
            # 将拿到的uname到数据库查询
            if self.application.dbutil.isexists(name):
                self.write({'msg':'fail'})
            else:
                # 根据查询结果生成响应内容JSON格式
                self.write({'msg':'ok'})
        else:
            avatar = self.application.dbutil.hasavatar(name)
            self.write({'msg':avatar})



class LoginModule(UIModule):
    def render(self, *args, **kwargs):
        r = ''
        if self.request.query:
            r = '用户名或密码错误'
        return self.render_string('mymodule/login_module.html', result=r)


class BlogModule(UIModule):
    def render(self, *args, **kwargs):
        s = Session(self.handler)
        uname = s['uname']
        BLOGS = self.handler.application.dbutil.getBlogs()
        return self.render_string('mymodule/blog_module.html', blogs=BLOGS, uname=uname)


class RegisterModule(UIModule):
    def render(self, *args, **kwargs):
        r = ''
        if self.request.query:
            err = self.request.query.split('=')[1]
            if err == 'duplicate':
                r = '这个用户名被抢占了,换一个试试吧'
            elif err == 'empty':
                r = '请将内容输入完整后重新提交!'
            else:
                r = '出错啦, 请重新输入!'
        return self.render_string('mymodule/register_module.html', result=r)


class PublishHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('publish.html')

    def post(self, *args, **kwargs):
        title = self.get_body_argument('title', None)
        label = self.get_body_argument('label', None)
        content = self.get_body_argument('mblog', None)
        s = Session(self)
        uname = s['uname']
        print(title,label,content,uname, s['islogin'])
        if title and content:
            try:
                self.application.dbutil.publishSave(uname, title, label, content)
            except Exception as e:
                self.redirect('/publish')
            else:
                self.redirect('/blog')
        else:
            self.redirect('/publish')
