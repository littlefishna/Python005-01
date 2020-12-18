学习笔记
```
作业
```
使用 Django 展示豆瓣电影中某个电影的短评和星级等相关信息：
```
1.要求使用 MySQL 存储短评内容（至少 20 条）以及短评所对应的星级；
```
```
2. 展示高于 3 星级（不包括 3 星级）的短评内容和它对应的星级；
```
```
3. （选做）在 Web 界面增加搜索框，根据搜索的关键字展示相关的短评。
```
-----------------------------------------------------
```
笔记
```
```
顺序简写:
python manage.py runserver
project/settings.py(获取配置信息) 
    -> project/urls.py(匹配路径信息，以及后续的app/urls.py) 
       -> app/urls.py(找到对应的views.xxxx)
          -> app/views.py(根据app/models.py 中的 表类,执行数据操作，与templates中变量名称对应)
```
```
项目目录中的文件意义：
settings.py : 总体配置信息(项目信息、数据库访问、tempaltes等信息)
urls.py : 匹配浏览器提交的路径，指向匹配后对应的app的views.py

app目录中文件意义：
models.py : 命令行 python manage.py inspectdb >> doubanProject/models.py ，依据 settings.py 中DATABASES设置
生成库中表的 类(包含字段信息等)，供 views.py 中 访问处理数据库表数据
urls.py : Project 中的 urls.py 导入的就是这个 urls.py , 指向 views.py 中的函数
views.py : 怎么访问数据，怎么处理数据，返回什么数据
```
```
执行 python manage.py migrate ，其中mysql用户需要以下权限
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, REFERENCES, INDEX, ALTER ON `test`.* TO 'pyuser'@'192.168.109.%'
其中 REFERENCES, INDEX, ALTER 权限 是根据报错，后来添加的
python manage.py migrate 命令执行成功后，settings中指定的mysql库中，会创建10个表
```
```
编辑 models.py 文件，改变模型。
运行 python manage.py makemigrations 为模型的改变生成迁移文件。
运行 python manage.py migrate 来应用数据库迁移。

重点！！！：
已经存在表结构，根据表结构，生成对应的model信息
python manage.py inspectdb >> doubanProject/models.py

宜居models.py 生成对象
python manage.py makemigrations doubanProject

windows 下，修改完 models.py 或者 views.py 记得保存，不保存情况下，不生效，会影响排错
```
```
条件筛选
n = mv.objects.all().filter(start__gt=3)
all() 返回的 QuerySet 包含了数据表中所有的对象。虽然，大多数情况下，你只需要完整对象集合的一个子集。
要创建一个这样的子集，你需要通过添加过滤条件精炼原始 QuerySet。两种最常见的精炼 QuerySet 的方式是：

filter(**kwargs)
返回一个新的 QuerySet，包含的对象 满足 给定查询参数。

exclude(**kwargs)
返回一个新的 QuerySet，包含的对象 不满足 给定查询参数。

```