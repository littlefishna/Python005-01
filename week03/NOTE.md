学习笔记
\1. 在 Linux 环境下，安装 MySQL5.6 以上版本，修改字符集为 UTF8mb4 并验证，新建一个数据库 testdb，并为该数据库增加远程访问的用。

- 将修改字符集的配置项、验证字符集的 SQL 语句作为作业内容提交

  ```
  set global character_set_server=utf8mb4;
  set global collation_server=utf8mb4_general_ci;
  ```

- 将增加远程用户的 SQL 语句作为作业内容提交

  ```
  GRANT SELECT,DELETE,UPDATE,INSERT on test.* to 'pyuser'@'192.168.109.%' identified by 'pyuser'
  ```

\2. 使用 sqlalchemy ORM 方式创建如下表，使用 PyMySQL 对该表写入 3 条测试数据，并读取:

- 用户 id、用户名、年龄、生日、性别、学历、字段创建时间、字段更新时间

- 将 ORM、插入、查询语句作为作业内容提交

  ```python
  #!/usr/bin/env python3
  import pymysql
  from datetime import datetime
  from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, DateTime
  from sqlalchemy.orm import sessionmaker
  from sqlalchemy.ext.declarative import declarative_base
  
  Base = declarative_base()
  
  class userinfo_table(Base):
      __tablename__ = 'bookorm'
      id = Column(Integer(), primary_key=True)
      name = Column(String(50), index=True)
      age = Column(Integer())
      birthday =Column(DateTime())
      sex = Column(String(5))
      educ = Column(String(5))
      create_time = Column(DateTime())
  
  engine = create_engine("mysql+pymysql://pyuser:pyuser@192.168.109.129:3306/test?charset=utf8mb4", echo=True)
  
  # 创建元数据
  metadata = MetaData(engine)
  
  # 用户 id、用户名、年龄、生日、性别、学历、字段创建时间、字段更新时间
  userinfo_table = Table('userinfo', metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String(20)),
                         Column('age', Integer),
                         Column('birthday', String(20)),
                         Column('sex', String(5)),
                         Column('educ',String(5)),
                         Column('create_time',DateTime()),
                         Column('modify_time',DateTime(),default=datetime.now())
                         )
  
  SessionClass = sessionmaker(bind=engine)
  session = SessionClass()
  
  row1 = userinfo_table(id=1,name='xxx',age=16,birthday='xxxx-xx-xx',sex='M',educ='B',create_time=datetime.now())
  row2 = userinfo_table(id=2,name='yyy',age=26,birthday='xxxx-xx-xx',sex='F',educ='S',create_time=datetime.now())
  row3 = userinfo_table(id=3,name='zzz',age=24,birthday='xxxx-xx-xx',sex='M',educ='A',create_time=datetime.now())
  
  try:
      metadata.create_all()
      session.add(row1)
      session.add(row2)
      session.add(row3)
  except Exception as e:
      print("have some error : {}".format(e))
  
  ```



\3. 为以下 sql 语句标注执行顺序：

```
SELECT DISTINCT player_id, player_name, count(*) as num 
FROM player JOIN team ON player.team_id = team.team_id 
WHERE height > 1.80 
GROUP BY player.team_id 
HAVING num > 2 
ORDER BY num DESC 
LIMIT 2
```

顺序

```
加载目标表信息 team、player
按player.team_id = team.team_id条件，循环匹配，生成join结果集
按 WHERE height > 1.80 , 过滤结果集
GROUP BY player.team_id HAVING num > 2，生成结果集
ORDER BY num DESC LIMIT 2，对结果集进行倒序排序，找到num最大的两个返回
结束
```



\4. 以下两张基于 id 列，分别使用 INNER JOIN、LEFT JOIN、 RIGHT JOIN 的结果是什么?

**Table1**

id name

1 table1_table2

2 table1

**Table2**

id name

1 table1_table2

3 table2

举例: INNER JOIN

```
SELECT Table1.id, Table1.name, Table2.id, Table2.name
FROM Table1
INNER JOIN Table2
ON Table1.id = Table2.id;

结果：取 满足 Table1.id = Table2.id 条件的所有值；交集
```

LEFT JOIN

```
SELECT Table1.id, Table1.name, Table2.id, Table2.name
FROM Table1
LEFT JOIN Table2
ON Table1.id = Table2.id;

结果： Table1 存在，但Table2 不存在的值也显示，但Table2.id，Table2.name 列为NULL
```

RIGHT JOIN

```
SELECT Table1.id, Table1.name, Table2.id, Table2.name
FROM Table1
RIGHT JOIN Table2
ON Table1.id = Table2.id;

结果： Table2 存在，但Table1 不存在的值也显示，但Table1.id，Table1.name 列为NULL
```

\5. 使用 MySQL 官方文档，学习通过 sql 语句为上题中的 id 和 name 增加索引，并验证。根据执行时间，增加索引以后是否查询速度会增加？请论述原因，并思考什么样的场景下增加索引才有效。

```
mysql > ALTER TABLE Table1 add index idx1(`id`)
场景：业务sql对于Table1表的SELECT的情况为-> 以id列的值为条件进行查询

mysql > ALTER TABLE Table1 add index idx2(`name`)
场景：业务sql对于Table1表的SELECT的情况为-> 以name列的值为条件进行查询，若name列为字符格式，索引创建优先满足distict(left(name,N)),查找最优左前缀重复度创建索引

mysql > ALTER TABLE Table1 add index idx3(`id`,`name`)
场景：业务sql对于Table1表的SELECT的情况为-> 以id列值为条件，查找对应的name列的值，开启下推情况下，效果明显
```

\6. 张三给李四通过网银转账 100 极客币，现有数据库中三张表：

一张为用户表，包含用户 ID 和用户名字，另一张为用户资产表，包含用户 ID 用户总资产，
第三张表为审计用表，记录了转账时间，转账 id，被转账 id，转账金额。

- 请合理设计三张表的字段类型和表结构；

  ```sql
  CREATE TABLE `user_info` (`id` int primary key auto_increment,`u_id` varchar(30) NOT NULL,`u_name` varchar(30) NOT NULL)
  CREATE TABLE `user_assets` (`id` int primary key auto_increment,`u_id` varchar(30) NOT NULL,`u_assets` DOUBLE(12,3))
  CREATE TABLE `user_audit` (`id` int primary key auto_increment,`from_uid` varchar(30) NOT NULL,`to_uid` varchar(30) NOT NULL,`transfer_accounts` DOUBLE(12,3),`trans_time` timestamp DEFAULT CURRENT_TIMESTAMP)
  ```



- 请实现转账 100 极客币的 SQL(可以使用 pymysql 或 sqlalchemy-orm 实现)，张三余额不足，转账过程中数据库 crash 等情况需保证数据一致性。

