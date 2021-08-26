# coding: utf-8

# 事前に pip install mysqlclient を実行すること

DB_USER     = ''
DB_PASSWORD = ''
DB_HOST     = ''

import MySQLdb

def show_processlist():
    """ 接続サンプル """

    # 接続する
    con = MySQLdb.connect(
            user=DB_USER,
            passwd=DB_PASSWORD,
            host=DB_HOST,
            charset="utf8"
    )

    # カーソルを取得する
    cur = con.cursor()

    # クエリを実行する
    sql = "show processlist"
    cur.execute(sql)

    # 実行結果をすべて取得する
    rows = cur.fetchall()

    # 一行ずつ表示する
    for row in rows:
        print(row)

    cur.close()
    con.close()

if __name__ == "__main__":
    show_processlist()