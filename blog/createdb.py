import configparser
import pymysql

sql_user = '''create table tb_user(
    user_id int auto_increment,
    user_name varchar(32) not null,
    user_password varchar(64) not null,
    user_avatar varchar(128) default null,
    user_city varchar(32) not null,
    user_createdat datetime default current_timestamp,
    user_updatedat datetime default current_timestamp on update current_timestamp,
    primary key(user_id),
    unique(user_name))default charset=utf8;'''

sql_blog = '''create table tb_blog(
    blog_id int auto_increment,
    blog_user_id int not null,
    blog_title varchar(100) not null,
    blog_content varchar(1024) not null,
    blog_createdat datetime default current_timestamp,
    blog_updatedat datetime default current_timestamp on update current_timestamp,
    primary key(blog_id),
    foreign key(blog_user_id) references tb_user(user_id) on delete cascade on update cascade)default charset=utf8;'''

sql_tag = '''create table tb_tag(
    tag_id int auto_increment,
    tag_content varchar(16) not null,
    primary key(tag_id))default charset=utf8;'''

sql_blog_tag = '''create table tb_blog_tag(
    blog_tag_id int auto_increment,
    rel_blog_id int not null,
    rel_tag_id int not null,
    primary key(blog_tag_id),
    foreign key(rel_blog_id) references tb_blog(blog_id) on delete cascade on update cascade,
    foreign key(rel_tag_id) references tb_tag(tag_id) on delete cascade on update cascade)default charset=utf8;'''

sql_comment = '''create table tb_comment(
    comment_id int auto_increment,
    comment_blog_id int not null,
    comment_user_id int not null,
    comment_content varchar(256) not null,
    comment_createdat datetime default current_timestamp,
    comment_updatedat datetime default current_timestamp on update current_timestamp,
              primary key(comment_id),
    foreign key(comment_blog_id) references tb_blog(blog_id) on delete cascade on update cascade,foreign key(comment_user_id) references tb_user(user_id) on delete cascade on update cascade)default charset=utf8;'''

sqls = [sql_blog, sql_tag, sql_blog_tag, sql_comment]

settings = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '123456',
            'database': 'blog_db',
            'charset': 'utf8'
        }


def create_tables():
    # 建立连接
    connection = pymysql.connect(**settings)
    # 获取游标
    cursor = connection.cursor()
    for sql in sqls:
        cursor.execute(sql)
    cursor.close()
    connection.close()


if __name__ == '__main__':
    create_tables()