#!/usr/bin/env python3
# 请实现转账 100 极客币的 SQL(可以使用 pymysql 或 sqlalchemy-orm 实现)
# 张三余额不足，转账过程中数据库 crash 等情况需保证数据一致性

import pymysql
from dbutils.pooled_db import PooledDB


def connect2DB():
    db_config = {
        "host": "192.168.109.129",
        "port": 3306,
        "user": "pyuser",
        "passwd": "pyuser",
        "db": "test",
        "charset": "utf8mb4",
        "maxconnections": 0,  # 连接池允许的最大连接数
        "mincached": 4,  # 初始化时连接池中至少创建的空闲的链接,0表示不创建
        "maxcached": 0,  # 连接池中最多闲置的链接,0不限制
        "maxusage": 5,  # 每个连接最多被重复使用的次数,None表示无限制
        "blocking": True  # 连接池中如果没有可用连接后是否阻塞等待 True 等待; False 不等待然后报错
    }
    try:
        spool = PooledDB(pymysql, **db_config)

        conn = spool.connection()
        cursor = conn.cursor()
    except Exception as err:
        return '', '', err

    return conn, cursor, False

# 审计记录函数
def wriAudit(conn,cur,fromAccount,toAccount,transCount):
    sql = "INSERT INTO user_audit(from_uid,to_uid,transfer_accounts) VALUES('{}','{}',{})".format(fromAccount,toAccount,transCount)

    try:
        cur.execute(sql)
        conn.commit()
    except:
        conn.rollback()

# 转账行为函数
def transAccount(conn, cur, fromuser, touser, transCount):
    sql_fromuser_id = "select u_id from user_info where u_name='{}'".format(fromuser)
    sql_touser_id = "select u_id from user_info where u_name='{}'".format(touser)

    cur.execute(sql_fromuser_id)
    fromuser_id = cur.fetchone()[0] # 当前用户必定存在
    cur.execute(sql_touser_id)
    touser_id = cur.fetchone()
    # 判断目标用户是否存在
    if touser_id is None:
        print("target user not exist")
    else: # 目标用户存在则开始准备转账
        # 查询fromuser余额是否足够转账金额
        sql_SELECTAssets_fromuser = "SELECT a.u_assets FROM user_assets a JOIN user_info i ON a.u_id = i.u_id WHERE i.u_name='{}'".format(
            fromuser)

        cur.execute(sql_SELECTAssets_fromuser)
        fromuser_account_Balance = cur.fetchone()[0]

        if transCount <= fromuser_account_Balance:
            try:
                sql_UPDATEfromuser = "UPDATE user_assets SET u_assets = u_assets - {} WHERE u_id = '{}'".format(transCount,fromuser_id)
                sql_UPDATEtouser = "UPDATE user_assets SET u_assets = u_assets + {} WHERE u_id = '{}'".format(transCount,touser_id[0])
                cur.execute(sql_UPDATEfromuser)
                conn.commit()
                cur.execute(sql_UPDATEtouser)
                conn.commit()

                wriAudit(conn=conn,cur=cur,fromAccount=fromuser,toAccount=touser,transCount=transCount)
            except:
                conn.rollback()
        else:
            print("FAILED:Not enough money")

    cur.close()
    conn.close()


if __name__ == '__main__':
    conn, cursor, err = connect2DB()
    if err:
        print(err)
    else:
        # 连接未报错，开始执行转账动作
        transAccount(conn=conn, cur=cursor, fromuser='zhang3', touser='li4',transCount=211.6)

