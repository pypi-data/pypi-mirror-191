import pymysql
import pymssql
import pymongo
from pymoran.strtool import StrClass


class MySQLClient:
    def __init__(self, dbdata: dict) -> None:
        '''
        初始化数据库连接
        :param dbdata(host 主机地址,user 用户名,password 密码,database 数据库,port 端口，默认3306)
        :return {bool} True/False
        '''
        # 打开数据库连接
        self.conn = pymysql.connect(
            host=dbdata['host'],
            user=dbdata['user'],
            password=dbdata['password'],
            database=dbdata['database'],
            port=dbdata['port']
        )
        # 使用cursor()方法获取操作游标
        self.cursor = self.conn.cursor()
        self.strclass = StrClass()

    def close(self):
        self.conn.close()

    def creat_table(self, name: str, field: list, close: bool = True):
        '''
        创建表
        :param name 表名
        :param field 字段列表，例：['id INT AUTO_INCREMENT PRIMARY KEY','name varchar(255)']
        :return {bool} True/False
        '''
        result = False
        sql = 'create table %s (%s)' % (name, (',').join(field))
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            result = True
        except:
            # 如果发生错误则回滚
            self.conn.rollback()
            result = False
        if close:
            self.close()
        return result

    def custom_query(self, query: str, args: tuple=(), close: bool = True):
        '''
        自定义查询语句
        :param table 表名
        :param data 需要插入的数据
        :param close 是否自动关闭数据库连接，默认True
        :return {bool} True/False
        '''
        result = False

        try:
            # 执行sql语句
            self.cursor.execute(query, args)
            # 提交到数据库执行
            self.conn.commit()
            result = True
        except:
            # 如果发生错误则回滚
            self.conn.rollback()
            result = False
        if close:
            self.close()
        return result
        
    def custom_fetch(self, query: str, args: tuple = (), close: bool = True):
        '''
        查询数据，查询条件数据建议使用html_escape转码保证数据查询安全
        :param query 自定义查询语句
        :param args 查询参数元组
        :param close 是否自动关闭数据库连接，默认True
        :return {list} 如没有查询结果则返回None
        '''
        try:
            # 执行SQL语句
            self.cursor.execute(query,args)
            # 获取所有记录列表
            results = self.cursor.fetchall()
        except:
            print("Error: unable to fetch data")
        # 关闭数据库连接
        if close:
            self.close()
        # 没有查询结果则返回None
        if len(results) == 0:
            return None
        return results

    def insert(self, table: str, data: dict, close: bool = True):
        '''
        插入数据，插入的数据内容无需做特殊安全处理，方法内均进行了html转码保存数据
        :param table 表名
        :param data 需要插入的数据
        :param close 是否自动关闭数据库连接，默认True
        :return {bool} True/False
        '''
        result = False
        # 列
        col = []
        # 行
        row = []
        for d in data.keys():
            col.append(d)
            value=self.strclass.html_escape(data[d])
            value=value.replace('\\','\\\\')
            row.append('"'+value+'"')
        sql = 'INSERT INTO %s (%s) VALUES (%s)' % (
            table,
            ','.join(col),
            ','.join(row)
        )
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            result = True
        except:
            # 如果发生错误则回滚
            self.conn.rollback()
            result = False
        if close:
            self.close()
        return result

    def insert_many(self,
                    table: str,
                    field: list,
                    data: list,
                    close: bool = True):
        '''
        插入数据，插入的数据内容无需做特殊安全处理，方法内均进行了html转码保存数据
        :param table 表名
        :param field 需要插入数据的字段列表
        :param data 需要插入的多条数据[[],[],[]]
        :param close 是否自动关闭数据库连接，默认True
        :return {bool} True/False
        '''
        result = False
        values = []
        for d in data:
            val = '(%s)' % (','.join(str(v) if type(v)!= str else "'"+self.strclass.html_escape(v).replace('\\','\\\\')+"'" for v in d))
            values.append(val)
        sql = 'INSERT INTO %s (%s) VALUES %s' % (table, ','.join(field),
                                                 ','.join(values))
        try:
            # 如果连接断开则重连
            self.conn.ping(reconnect=True)
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            result = True
        except:
            # 如果发生错误则回滚
            self.conn.rollback()
            result = False
        if close:
            self.close()
        return result

    def fetch(self, fields: list, table: str, query: str = '', orderby: dict = None, limit: int = 0, close: bool = True):
        '''
        查询数据，查询条件数据建议使用html_escape转码保证数据查询安全
        :param fields 要查询的字段名
        :param table 表名
        :param query 查询条件，默认为空
        :param orderby 排序，默认为空，例：{'sort':'desc'}
        :param limit 查询条数，默认0则不限制条数
        :param close 是否自动关闭数据库连接，默认True
        :return {list} 如没有查询结果则返回None
        '''
        where_str = ''
        if query != '':
            where_str = 'WHERE %s' % query
        orderby_str = ''
        if orderby != None:
            orderby_arr = []
            for key in orderby.keys():
                orderby_arr.append('%s %s' % (key, orderby[key]))
            orderby_str = 'ORDER BY ' + ','.join(orderby_arr)
        limit_str=''
        if limit!=0:
            limit_str='limit %s' % limit
        sql = 'SELECT %s FROM %s %s %s %s' % (
            ','.join(fields),
            table,
            where_str,
            orderby_str,
            limit_str
        )
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
        except:
            print("Error: unable to fetch data")
        # 关闭数据库连接
        if close:
            self.close()
        # 没有查询结果则返回None
        if len(results) == 0:
            return None
        # 转化查询结果为list
        res_data = []
        col_count = len(fields)
        for result in results:
            col_data = {}
            for col in range(col_count):
                # 处理查询条件中特殊字符``
                field = fields[col].replace('`', '')
                col_data[field] = result[col]
            res_data.append(col_data)
        return res_data

    def fetch_count(self, table: str, query: str = '', close: bool = True):
        '''
        查询数据结果条数，查询条件数据建议使用html_escape转码保证数据查询安全
        :param table 表名
        :param query where后的查询条件，例：id=1 and name='张三'
        :param close 是否自动关闭数据库连接，默认True
        return:int 结果条数
        '''
        where_str = ''
        if query != '':
            where_str = 'WHERE %s' % query
        sql = 'SELECT count(*) FROM %s %s' % (
            table,
            where_str
        )
        results = (0,)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchone()
        except:
            print("Error: unable to fetch data")
        # 关闭数据库连接
        if close:
            self.close()
        # 没有查询结果则返回None
        return results[0]

    def update(self, table: str, set: dict, query: str = '', close: bool = True):
        '''
        更新数据，插入内容均自动做html_escape处理
        :param table 表名
        :param set 需要修改的内容
        :param query 查询条件，默认为空
        :param close 是否自动关闭数据库连接，默认True
        :return {bool} True/False
        '''
        result = False
        where_str = ''
        if query != '':
            where_str = 'WHERE %s' % query
        set_list = []
        for key in set.keys():
            value = self.strclass.html_escape(set[key])
            # 将字符串中的\替换为\\，防止插入mysql时\符号消失
            value = value.replace('\\', '\\\\')
            set_list.append(
                '%s="%s"' % (key, value)
            )
        sql = 'UPDATE %s SET %s %s' % (
            table,
            ','.join(set_list),
            where_str
        )
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            result = True
        except:
            # 发生错误时回滚
            self.conn.rollback()
            result = False
        # 关闭数据库连接
        if close:
            self.close()
        return result

    def delete(self, table: str, query: str = '', close: bool = True):
        '''
        删除数据，查询条件数据建议使用html_escape转码保证数据查询安全
        :param table 表名
        :param query 查询条件，默认为空
        :param close 是否自动关闭数据库连接，默认True
        :return {bool} True/False
        '''
        result = False
        where_str = ''
        if query != '':
            where_str = 'WHERE %s' % query
        sql = 'DELETE FROM %s %s' % (
            table,
            where_str
        )
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            result = True
        except:
            # 发生错误时回滚
            self.conn.rollback()
            result = False
        # 关闭数据库连接
        if close:
            self.close()
        return result

class MSSQLClient:
    def __init__(self,dbdata:dict) -> None:
        '''
        初始化数据库连接
        :param dbdata 连接配置，包含server，database
        '''
        self.conn=pymssql.connect(
            server=dbdata['server'],
            database=dbdata['database']
        )
        self.cursor=self.conn.cursor()

    def close(self):
        self.conn.close()

    def find(self,close: bool = True):
        data=[]
        # 关闭数据库连接
        if close:
            self.close()
        return data

    def delete(self,sql,close:bool=True):
        '''
        删除数据，查询条件数据建议使用html_escape转码保证数据查询安全
        :param table 表名
        :param query 查询条件，默认为空
        :param close 是否自动关闭数据库连接，默认True
        :return {bool} True/False
        '''

    def updata(self,sql,close:bool=True):
        # self.cursor.execute(sql)
        # self.conn.commit()
        # 关闭数据库连接
        if close:
            self.close()
        return True

class MongodbClient:
    def __init__(self, db_name:str, client_url:str):
        '''
        初始化数据库连接
        :param db_name 数据库名称
        :param client_url 数据库地址
        '''
        self.client = pymongo.MongoClient(client_url)
        self.db = self.client[db_name]

    def creatDict(self, colName, dictData):
        col = self.db[colName]
        result = col.insert_one(dictData)
        return result

    def insert_one(self, colName, data):
        col = self.db[colName]
        result = col.insert_one(data)
        if result:
            return True
        return False

    def insert_many(self, colName, data):
        col = self.db[colName]
        result = col.insert_many(data)
        return result.inserted_ids

    def find_count(self, colName: str, query: dict):
        col = self.db[colName]
        result = col.count_documents(query)
        return result

    def find_one(self, colName, query, dataname):
        col = self.db[colName]
        result = col.find_one(query, dataname)
        return result

    def find(self, colName, query, dataname, sort_name='_id', sort=1, skip: int = 0, limit: int = 100):
        col = self.db[colName]
        result = col.find(query, dataname).sort(sort_name, sort).skip(skip).limit(limit)
        return result

    def update_one(self, colName, query, data):
        col = self.db[colName]
        result = col.update_one(query, {"$set": data})
        return result

    def delete_one(self, colName: str, query: dict):
        '''
        删除操作
        :param colName 需要操作的表名称
        :param query 操作条件
        return {bool} True/False
        '''
        col = self.db[colName]
        result = col.delete_one(query)
        if result.deleted_count > 0:
            return True
        return False

    def delete_many(self, colName: str, query: dict):
        '''
        删除操作
        :param colName 需要操作的表名称
        :param query 操作条件
        return {bool} True/False
        '''
        col = self.db[colName]
        result = col.delete_many(query)
        if result.deleted_count > 0:
            return True
        return False


if __name__ == '__main__':
    pass
