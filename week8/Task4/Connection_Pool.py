#In[1]---------------------------------------------------------
import mysql.connector
from mysql.connector import pooling
import time

dbconfig = {
    "database": "website",
    "user": "root",
    "password": "12345678",
    "host": "localhost",
    # "port": "8080"
}

pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="website_db_pool",
                                                    pool_size=5,
                                                    pool_reset_session=True,
                                                    **dbconfig)


t = time.time()
connection = pool.get_connection()
# print(connection)
cursor = connection.cursor()
sql = "SELECT * FROM member"
cursor.execute(sql)
results = cursor.fetchall()
print(results)
# print(type(results))
cursor.close()
connection.close() # return connection to the pool.

print(f'coast:{time.time() - t:.8f}s')


#In[2]---------------------------------------------------------
import mysql.connector
from mysql.connector import pooling
import time

t2 = time.time()
website_db = mysql.connector.connect(
                                    user="root",
                                    password="12345678",
                                    host="localhost",
                                    database="website",
                                    charset="utf8mb4")
cursor = website_db.cursor()
"""
這邊修改成先用資料庫做篩選
如果回傳值是null就可以註冊
回傳有值的話就不能註冊

這邊前端傳過來的資料為 名稱、帳號、密碼、
"""

#查這個帳號有沒有在資料庫中
cursor.execute("select * from member;")
myresult = cursor.fetchall()#回傳所有資料庫指令結果
print(myresult)

print(f'coast:{time.time() - t2:.8f}s')








#In[3]---------------------------------------------------------
#     for row in results:
#         print(row)
#     cursor.close()
#     connection.close() # return connection to the pool.
#     print("Connection returned to pool.")
# else:
#     print("Failed to get connection from pool.")

# except mysql.connector.Error as err:
#     print(f"Error: {err}")
# finally:
#     if 'connection' in locals() and connection.is_connected():
#         connection.close() # return connection to the pool.
# %%
