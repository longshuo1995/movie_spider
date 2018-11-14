from flask import request, make_response
import time
import xml.etree.ElementTree as ET
import hashlib

from app import secure
from app.db_master import db_scheduler, mongo
from . import web


reply = """
<xml>
<ToUserName> <![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%s]]></Content>
</xml>
"""


def extract_wechat_msg(data):
    xml_recv = ET.fromstring(data)
    ToUserName = xml_recv.find('ToUserName').text
    FromUserName = xml_recv.find('FromUserName').text
    content = xml_recv.find('Content').text
    result = {
        'ToUserName': ToUserName,
        'FromUserName': FromUserName,
        'content': content,
    }
    return result


def verify_signature(data):
    my_signature = data.get('signature')
    my_timestamp = data.get('timestamp')
    my_nonce = data.get('nonce')
    my_echostr = data.get('echostr')

    token = secure.WECHAT_TOKEN
    data = [token, my_timestamp, my_nonce]
    data.sort()

    temp = ''.join(data)

    mysignature = hashlib.sha1(temp).hexdigest()

    if my_signature == mysignature:
        return my_echostr
    return ''


def make_reply(fromuser, touser, content):
    response = make_response(
        reply % (fromuser, touser, str(int(time.time())), content))
    return response


def get_content(keyword):
    mvs = db_scheduler.get_mvs(keyword)
    result = []
    for mv in mvs:
        temp = ''
        if mv.get('title'):
            temp += mv['title']
        if mv.get('director'):
            temp += ' 导演'+mv['director']
        # temp += ' <a href="http://140.143.163.73:80/movie/play?_id=%s">点击观看</a>' % mv['_id']
        temp += ' <a href="%s">点击观看</a>' % mongo.search_play_detail(mv['_id'])['type_playurl'][0][1]
        result.append(temp)
        suggestion = '\n\n搜索建议：多个关键词用空格分开更精准'
    return '\n'.join(result) + suggestion


@web.route("/wechat", methods=['GET', 'POST'])
def wechat():
    if request.method == 'POST':
        msg_info = extract_wechat_msg(request.data)
        FromUserName = msg_info['FromUserName']
        ToUserName = msg_info['ToUserName']
        keyword = msg_info['content']
        content = get_content(keyword)
        content = content.strip()
        if not content:
            content = "暂无搜索结果"

        return make_reply(FromUserName, ToUserName, content)

    if request.method == "GET":
        return "hello"

