import sqlite3
import config


class DbOpt:
    def __init__(self):
        self.dbpath = config.db_connect["db_file_path"]

    def __del__(self):
        self.dbpath = None

    def create_table(self, table_name):
        conn = sqlite3.connect(config.db_connect["db_file_path"])
        cur = conn.cursor()

        cur.execute("DROP TABLE IF EXISTS " + table_name)
        sql = "CREATE TABLE " + table_name + "("

        for key, value in config.table_definition.get(table_name).items():
            sql += key + " " + value + ","

        sql = sql[:-1] + ")"
        print(sql)
        cur.execute(sql)
        conn.close()

    # 初始化table
    def insert_table_data(self, table_name, table_data):
        conn = sqlite3.connect(config.db_connect["db_file_path"])
        # table data = config. dim_ data.get (table name)
        cur = conn.cursor()
        sql = "INSERT INTO " + table_name + " VALUES ("  # (?, ?,?)
        for i in range(len(table_data[0])):
            sql += "?,"
        sql = sql[:-1] + ")"
        cur.executemany(sql, table_data)  # 使用同号作均占位待
        conn.commit()
        conn.close()

    def select_table_data(self, sqlquery):
        conn = sqlite3. connect(config.db_connect["db_file_path"])
        cur = conn.cursor()
        cur.execute(sqlquery)
        data_result = cur.fetchall()
        # print( cur.fetchall())# 返回所有查询结果
        conn.close()
        return data_result
