import os
import time
import math
import json
import random
import nonebot
import requests
import traceback
from flask import Flask, request
from main import API
from random import choice
from text_to_image import text_to_image
from flask import request, Flask
from revChatGPT import Chatbot, generate_uuid
from flask_apscheduler import APScheduler

pathogen = json.load(open("./device.json", encoding='utf-8'))["pathogen"]
path_two = json.load(open("./device.json", encoding='utf-8'))["path_two"]
path_three = json.load(open("./device.json", encoding='utf-8'))["path_three"]

with (open("./device.json", encoding='utf-8')) as jsonfile:
    config_data = json.load(jsonfile)
    qq_config = config_data["qq_bot"]
    chat_gpt_config = config_data["chatGPT"]
    qq_no = qq_config['qq_no']
    cqhttp_url = qq_config['cqhttp_url']

def menu():
    data = request.get_json()
    uurl = 'http://127.0.0.1:5700'
    #实现调用的四个指令
    message = data['message']
    message_id = data['message_id']
    message_type = data['message_type']
    uid = data['user_id']
    data['group_id'] = 114514
    group_id = data['group_id']
    banned_words = ['膜', '佬', '娇娇', '带带', '大佬', '巨佬','[CQ:face,id=297]','sb','巨神']
    if "survival_judgment" == message:
        API.send("exist")

    if str("[CQ:at,qq=%s]" % qq_no) in message:
        sender = request.get_json().get('sender')  # 消息发送者的资料
        #print("收到群聊消息：")
        message = str(message).replace(str("[CQ:at,qq=%s]" % qq_no), '')
        print(message)
        API.send(message)
        information = "这里是无何的机器人bot(◦˙▽˙◦)，你可以进行以下操作~\n\n" \
            "------Entertainment function------\n" \
            "   输入‘喵’生成猫猫图  \n" \
            "   输入‘猫猫’生成Capoo  \n" \
            "   输入‘setu’生成二次元图片\n" \
            "------Computing function------\n"\
            "   输入‘circle area’计算圆的面积\n" \
            "   输入‘sqrt’计算数字平方根\n" \
            "   输入‘square’计算数字平方\n"
        API.send(information+ "\n[CQ:at,qq="+str(uid)+"]"+" 说出你的想法吧 "+ '[CQ:face,id=318]')

    if 'menu' == message:
        msg = "这里是无何的机器人bot(◦˙▽˙◦)，你可以进行以下操作~\n\n" \
            "------Entertainment function------\n" \
            "   输入‘喵’生成猫猫图  \n" \
            "   输入‘猫猫’生成Capoo  \n" \
            "   输入‘setu’生成二次元图片\n" \
            "------Computing function------\n"\
            "   输入‘circle area’计算圆的面积\n" \
            "   输入‘sqrt’计算数字平方根\n" \
            "   输入‘square’计算数字平方\n"
        API.send(msg)

    elif message == 'circle area':
        API.send("Please enter the radius of the circle (in meters)")
        radius = API.reply(message_id)
        if "timeout" in radius:
            if message_type == 'group':
                API.send("[CQ:at,qq=" + str(uid) + "]" + "Reply timeout")
            else:
                API.send("[CQ:at,qq=" + str(uid) + "]" + "Reply timeout")
        else:
            try:
                radius = float(radius)
                area = 3.14 * (radius ** 2)
                API.send("[CQ:at,qq=" + str(uid) + "]" + "The area of the circle is: " + str(area) + " square meters ")
            except ValueError:
                API.send("[CQ:at,qq=" + str(uid) + "]" + "Please enter a valid radius value!")

    elif message == 'sqrt':
        API.send("请输入一个数字")
        num = API.reply(message_id)
        if "超时" in num:
            if message_type == 'group':
                API.send("[CQ:at,qq=" + str(uid) + "]" + "回复超时")
            else:
                API.send("[CQ:at,qq=" + str(uid) + "]" + "回复超时")
        else:
            try:
                num = float(num)
                result = math.sqrt(num)
                API.send("[CQ:at,qq=" + str(uid) + "]" + str(num) + "的平方根为:" + str(result) )
            except ValueError:
                API.send("[CQ:at,qq=" + str(uid) + "]" + "请输入正确的数字！")

    elif 'square' == message:
        API.send("请输入数字")
        number = API.reply(message_id)
        if "超时" in number:
            if message_type == 'group':
                API.send("[CQ:at,qq=" + str(uid) + "]" + "回复超时")
            else:
                API.send("[CQ:at,qq=" + str(uid) + "]" + "回复超时")
        else:
            try:
                number = float(number)
                result = number ** 2
                API.send("[CQ:at,qq=" + str(uid) + "]" + str(number) + "的平方为:" + str(result) )
            except ValueError:
                API.send("[CQ:at,qq=" + str(uid) + "]" + "请输入正确的数字！")


    elif '喵' == message:
        setu_list = os.listdir(pathogen)
        local_img_url = "[CQ:image,file=file:///" + pathogen + "/" + choice(setu_list) + "]"
        API.send("[CQ:at,qq="+str(uid)+"]"+local_img_url)

    elif 'setu' == message:
        setu_list = os.listdir(path_two)
        local_img_url = "[CQ:image,file=file:///" + path_two + "/" + choice(setu_list) + "]"
        API.send("[CQ:at,qq="+str(uid)+"]"+local_img_url)

    elif '猫猫' == message:
        setu_list = os.listdir(path_three)
        local_img_url = "[CQ:image,file=file:///" + path_three + "/" + choice(setu_list) + "]"
        API.send("[CQ:at,qq="+str(uid)+"]"+local_img_url)

    elif message in banned_words:
        rand = random.randint(0, 8)
        requests.get(url=uurl + '/delete_msg?message_id={0}'.format(message_id))
        requests.get(url=uurl + '/send_group_msg?group_id={0}&message={1}'.format(group_id, r'[CQ:at,' r'qq=' + str(
            uid) + r']' +' 违禁词警告\n群里严禁膜文化！！' +'[CQ:face,id=11]'))


    else:
        print('error')
    return "OK"

