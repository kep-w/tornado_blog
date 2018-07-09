import pymysql


class DBUtil:
    def __init__(self, **kwargs):
        # 获取数据库连接的参数,并建立连接
        # 为连接参数设置缺省默认值
        user = kwargs.get('user', 'root')
        password = kwargs.get('password', '123456')
        host = kwargs.get('host', 'localhost')
        port = kwargs.get('port', 3306)
        database = kwargs.get('database', 'blog_db')
        charset = kwargs.get('charset', 'utf8')
        self.db = pymysql.connect(user=user, password=password, host=host, port=port, database=database, charset=charset)
        if self.db:
            self.cursor = self.db.cursor()
        else:
            raise Exception('数据库连接参数有误')

    def loginSuccess(self, uname, upwd):
        # 根据输入用户名和密码判断是否登录成功
        sql = 'select count(*) from tb_user where user_name=%s and user_password=%s;'
        params = (uname, upwd)
        self.cursor.execute(sql, params)
        result = self.cursor.fetchone()
        if result[0]:
            return True
        else:
            return False

    def registSave(self, uname, upwd, avatar, city):
        # 根据用户输入注册信息完成注册
        sql = 'insert into tb_user(user_name, user_password, user_avatar, user_city) values(%s, %s, %s, %s)'
        params = (uname, upwd, avatar, city)
        try:
            self.cursor.execute(sql, params)
            # self.db.commit()
            self.cursor.connection.commit()
        except Exception as e:
            err = str(e)
            err = err.split(',')[0][1:]
            r = 'dberror'
            if err == '1062':
                r = 'duplicate'
            raise Exception(r)

    def getBlogs(self):
        # 取出数据库中与博客相关的内容
        # 组织成正确的数据格式返回
        sql = '''select user_avatar, user_name, blog_title, blog_content, blog_updatedat, tg, c
            from (select user_name, user_avatar,blog_id,blog_title, blog_content,blog_updatedat,tg
                from tb_user
                join (
                    select blog_user_id, blog_id, blog_title, blog_content, blog_updatedat,tg
                    from tb_blog
                    left join (
                        select rel_blog_id, group_concat(tag_content)tg
                        from tb_tag
                        join (select rel_blog_id,rel_tag_id
                        from tb_blog_tag)t
                        on rel_tag_id = tag_id
                        group by rel_blog_id
                        )t2
                    on blog_id = rel_blog_id
                )t3
                on blog_user_id = user_id)t4
            left join (select comment_blog_id, count(*)c
            from tb_comment
            group by comment_blog_id )t5
            on comment_blog_id = blog_id
            order by blog_updatedat DESC'''
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        blogs = []
        for r in result:
            blog = {}
            blog['avatar'] = r[0]
            blog['author'] = r[1]
            blog['title'] = r[2]
            blog['content'] = r[3]
            blog['tags'] = r[4]
            blog['count'] = r[5]
            blogs.append(blog)
        return blogs

    def isexists(self, uname):
        # 根据传入用户名, 判断用户是否存在
        sql = 'select count(*) from tb_user where user_name=%s'
        params = (uname,)
        self.cursor.execute(sql, params)
        result = self.cursor.fetchone()
        if result[0]:
            return True
        else:
            return False

    def hasavatar(self, uname):
        # 根据用户名查询头像
        sql = 'select user_avatar from tb_user where user_name=%s'
        params = (uname,)
        self.cursor.execute(sql, params)
        result = self.cursor.fetchone()
        # 如果输入的用户不存在, result是none,所以先判断
        if result:
            if result[0]:
                return result[0]
            else:
                return 'default_avatar.png'
        else:
            return 'default_avatar.png'

    def getuid(self, uname):
        sql = 'select user_id from tb_user where user_name=%s'
        params = (uname,)
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()[0]

    def getblogid(self, title):
        sql = 'select blog_id from tb_blog where blog_title=%s'
        params = (title,)
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()[0]

    def publishSave(self, uname, title, label, content):
        userid = self.getuid(uname)
        sql = 'insert into tb_blog(blog_user_id, blog_title, blog_content) values (%s, %s, %s)'
        params = (userid, title, content)
        self.cursor.execute(sql, params)
        self.cursor.connection.commit()
        bid = self.getblogid(title)
        sql_bt = 'insert into tb_blog_tag(rel_blog_id, rel_tag_id) values(%s,%s)'
        params = (bid, int(label))
        self.cursor.execute(sql_bt, params)
        self.cursor.connection.commit()

    def close(self):
        self.cursor.close()
        self.db.close()
