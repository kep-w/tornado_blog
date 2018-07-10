# 基于tornado的个人博客
应用tornado的功能实现个人博客的注册登录, 头像上传展示, ajax局部验证 及 列表展示动态, 发布动态
- 所用技术点涵盖:
  * python3
  * tornado
  * MySQL, 及复杂的SQL语句实现多表(5表)联查
  * ajax 实现头像动态查询展示, 用户验证
  * hashlib 及 uuid 对密码的算法转换
  * session 保存状态
  * 配置文件解析应用
  * HTML文件模板及模块化

- tornado运行
  * 运行前进行数据库的准备, 建库建表
  * 通过python3 tornadoserver.py 运行文件
