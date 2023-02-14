import sqlite3

conn = sqlite3.connect('bot.db')

print("数据库打开成功")

c = conn.cursor()
c.execute('''CREATE TABLE message
       (id INTEGER PRIMARY KEY AUTOINCREMENT,
       QQ           INT    NOT NULL,
       message        CHAR(500),
       message_id        CHAR(500),
       send_time        CHAR(500),
       message_type     CHAR(500),
       group_id         CHAR(500),
       SALARY         REAL);''')

print("数据表创建成功")
conn.commit()
conn.close()
