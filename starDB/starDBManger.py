'''
@Author: Alicespace
@Date: 2019-12-09 09:39:30
@LastEditTime: 2019-12-09 16:10:37
'''
import sqlite3


class DBTool(object):
    def __init__(self, table_name):
        """
        初始化函数，创建数据库连接
        """
        self.conn = sqlite3.connect('res/stars.db')
        self.c = self.conn.cursor()
        table = '(id integer,name text,mass text,radius text,texture text,model text,position text,velocity text)'
        self.initSql = 'create table if not exists ' + table_name + table
        self.c.execute(self.initSql)

    def executeUpdate(self, sql, ob):
        """
        数据库的插入、修改函数
        :param sql: 传入的SQL语句
        :param ob: 传入数据
        :return: 返回操作数据库状态
        """
        try:
            self.c.executemany(sql, ob)
            i = self.conn.total_changes
        except Exception as e:
            print('错误类型： ', e)
            return False
        finally:
            self.conn.commit()
        if i > 0:
            return True
        else:
            return False

    def executeDelete(self, sql, ob):
        """
        操作数据库数据删除的函数
        :param sql: 传入的SQL语句
        :param ob: 传入数据
        :return: 返回操作数据库状态
        """
        try:
            self.c.execute(sql, ob)
            i = self.conn.total_changes
        except Exception as e:
            return False
        finally:
            self.conn.commit()
        if i > 0:
            return True
        else:
            return False

    def executeQuery(self, sql, ob):
        """
        数据库数据查询
        :param sql: 传入的SQL语句
        :param ob: 传入数据
        :return: 返回操作数据库状态
        """
        test = self.c.execute(sql, ob)
        return test

    def close(self):
        """
        关闭数据库相关连接的函数
        :return:
        """
        self.c.close()
        self.conn.close()


'''
    db = DBTool()
    print("插入Student信息")
    name = input('输入姓名：')
    age = input('输入年龄：')
    ob = [(name, age)]
    sql = 'insert into stu (name, age) values (?,?)'
    T = db.executeUpdate(sql, ob)
    if T:
        print('插入成功！')
    else:
        print('插入失败！')
 
    print("通ID修改Student姓名信息")
    sql2 = 'UPDATE stu set name = ? where ID=?'
    id = input('输入需要修改的ID：')
    name = input('输入修改的Name：')
    ob = [(name, id)]
    T = db.executeUpdate(sql2, ob)
    if T:
        print('修改成功！')
    else:
        print('修改失败！')
         
    print("通ID删除Student信息")
    num = input('输入需要删除的学员ID:')
    sql2 = "DELETE from stu where ID=?"
    ob = [(num)]
    T = db.executeDelete(sql2, ob)
    if T:
        print('删除成功！')
    else:
        print('删除失败！')
 
    print("通姓名查询Student信息")
    sql = 'select * from stu where name=?'
    name = input('输入需要查询的学员姓名：')
    ob = [(name)]
    s = db.executeQuery(sql, ob)
    st = []
    for st in s:
        print('ID:', st[0], '  Name:', st[1], '  Age:', st[2])
    if any(st):
        pass
    else:
        print("输入有误，该学员不存在")
     
    # 关闭数据库连接
    db.close()'''