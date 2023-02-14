from flask import Flask, request
import requests
import menu
import sqlite3
import time
import json

'''这是导入的另一个文件，下面会讲到'''

app = Flask(__name__)


class API:
    @staticmethod
    def send(message):
        '''
        语法问题：将data字典中的"group_id"的值设置为你自身的群号。
        最后，你从data字典中读取了"group_id"的值并将它转换为字符串，并将它传递给了params字典
        错误做法：group_id = data['xxx'],如果你想要从data中读取group_id的值,应该将data['xxx']替换为data['group_id'],因为data['group_id']才是你需要的数据。
        在这个代码片段中,data['xxx']表示获取data字典中key为'xxx'的value,它并不能提供你想要的group_id的值.
        '''
        data = request.get_json()
        data['message_type']='group'
        message_type = data['message_type']
        if 'group' == message_type:
            #-
            data['group_id'] = 114514
            group_id = data['group_id']
            #-
            params = {
                "message_type": 'message_type',
                "group_id": str(group_id),
                "message": message
            }
        else:
            data['user_id']='114514'
            user_id = data['user_id']
            params = {
                "message_type": message_type,
                "user_id": user_id,
                "message": message
            }
        url = "http://127.0.0.1:5700/send_msg"

        requests.get(url, params=params)

    @staticmethod
    def save_message():
        data = request.get_json()
        uid = data['user_id']
        message = data['message']
        message_id = data['message_id']
        send_time = data['time']
        message_type = data['message_type']
        if message_type == 'group':
            group_id = data['group_id']
        else:
            group_id = "无"
        conn = sqlite3.connect("bot.db")
        c = conn.cursor()
        c.execute(
            "insert into message(QQ, message, message_id, send_time, message_type, group_id) values (?, ?, ?, ?, ?, ?)",
            (uid, message, message_id, send_time, message_type, group_id))
        conn.commit()
        conn.close()

    @staticmethod
    def reply(message_id):
        conn = sqlite3.connect("bot.db")
        c = conn.cursor()
        c.execute("SELECT * FROM message WHERE message_id = ?", (message_id,))
        results = c.fetchone()
        QQ = results[1]
        ID = results[0]
        group_id = results[6]
        message_type = results[5]
        num = ID + 1
        n = 0
        for i in range(60):
            n += 1
            try:
                c.execute("SELECT * FROM message WHERE id = ?", (num,))
                results = c.fetchone()
                new_QQ = results[1]
                new_group_id = results[6]
                new_message_type = results[5]
                if message_type == new_message_type == 'group':
                    if int(new_QQ) == int(QQ):
                        if int(new_group_id) == int(group_id):
                            new_message = results[2]
                            conn.commit()
                            conn.close()
                            return new_message
                        else:
                            num += 1
                            if n == 58:
                                conn.commit()
                                conn.close()
                                return "回复超时"
                            else:
                                time.sleep(1)
                                continue
                    else:
                        num += 1
                        if n == 58:
                            conn.commit()
                            conn.close()
                            return "回复超时"
                        else:
                            time.sleep(1)
                            continue
                elif message_type == new_message_type == 'private':
                    if int(new_QQ) == int(QQ):
                        new_message = results[2]
                        conn.commit()
                        conn.close()
                        return new_message
                    else:
                        num += 1
                        if n == 58:
                            conn.commit()
                            conn.close()
                            return "回复超时"
                        else:
                            time.sleep(1)
                            continue
                else:
                    num += 1
                    if n == 58:
                        conn.commit()
                        conn.close()
                        return "回复超时"
                    else:
                        time.sleep(1)
                        continue
            except:
                if n == 58:
                    conn.commit()
                    conn.close()
                    return "回复超时"
                else:
                    time.sleep(1)
                    continue

    @staticmethod
    def song(name_song):
        url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp"

        params = {
            'aggr': '1',
            'cr': '1',
            'flag_qc': '1',
            'p': '1',
            'n': '1',
            'w': name_song
        }

        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/103.0.0.0 Safari/537.36 "
        }

        res = requests.get(url, headers=headers, params=params)

        js = res.text.replace("callback(", '').replace(')', '')

        song_id = json.loads(js)['data']['song']['list'][0]['songid']

        API.send("[CQ:music,type=qq,id="+str(song_id)+"]")


@app.route('/', methods=["POST"])
def post_data():
    """下面的request.get_json().get......是用来获取关键字的值用的，关键字参考上面代码段的数据格式"""
    data = request.get_json()
    print(data)
    if data['post_type'] == 'message':
        API.save_message()
        message = data['message']
        print(message)
        menu.menu()
    else:
        print("暂不处理")

    return "OK"


if __name__ == '__main__':
    # 此处的 host和 port对应上面 yml文件的设置
    app.run(host='0.0.0.0', port=5701)  # 保证和我们在配置里填的一致
