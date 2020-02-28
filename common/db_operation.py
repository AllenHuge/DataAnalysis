import pymysql
import configparser
import os
from sqlalchemy import create_engine

# conn = pymysql.connect("localhost", "root", "huzhixue","test")
# cursor = conn.cursor()

#读取db配置信息
filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)),'config/')
filename = os.path.join(filepath, 'configure-db.properties')
config = configparser.ConfigParser()
config.read(filenames=filename)
my_host = config.get('mysql', 'host')
my_user = config.get('mysql', 'user')
my_password = config.get('mysql', 'password')
config.clear()

#mysql登录连接
def mysql_login(schema_name = ''):
    try:
        conn = pymysql.connect(my_host,my_user,my_password,schema_name)
        return conn
    except Exception as e:
        print('mysql登录失败：'+e)

#df插入mysql
def df2mysql(df,schema_name, table_name, chunksize=None, if_exists='replace',index=False,dtype=None):
    try:
        engine_file = 'mysql+pymysql://'+my_user+':'+my_password+'@'+my_host+'/'+schema_name
        engine = create_engine(engine_file)
        df.to_sql(  table_name
                  , engine
                  , if_exists=if_exists
                  , index=index
                  , chunksize = chunksize
                  , dtype = dtype
                  )
        return 0
    except Exception as e:
        print('插入mysql失败：'+e)


if __name__ == '__main__':
    # mysql数据库操作
    conn = mysql_login(schema_name = 'ext_data_stock')
    cursor = conn.cursor()
    sql = '''
    '''
    cursor.execute(sql)
    conn.commit()
    conn.close()

    print(conn)
