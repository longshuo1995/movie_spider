# coding=utf-8
import requests
from lxml import etree
from urllib.parse import unquote
import re

headers = {
   'Connection': 'close',
   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}
pattern_id = re.compile("id-(\d*)\.html")
pattern_down_url = re.compile("mac_url=unescape\('(.*)'\)")


def get_id(url):
    res = pattern_id.search(url)
    if res:
        return res.group(1)
    return ''


def get_xpath_content(xhtml, xpath):
    ress = xhtml.xpath(xpath)
    if ress:
        return ress[0]
    return ''


def extract_html(method, url, data):
    for i in range(10):
        if method == 'GET':
            ori = requests.get(url, headers=headers, data=data, timeout=35, verify=False)
        else:
            ori = requests.post(url, headers=headers, data=data, timeout=15, verify=False)
        b_html = ori.content
        if len(b_html) > 0:
            break
    if not b_html:
        return None
    try:
        html = b_html.decode(encoding='utf-8')
    except:
        try:
            html = b_html.decode(encoding='gbk')
        except:
            html = ori.text
    return html


def extract_mv_brief(param_strs):
    msgs = {
        "导演": "director",
        "主演": "main_star",
        "类型": "type",
        "地区": "area",
        "年份": "release_time",
        "简介": "brief",
    }
    result = dict()
    current_tp = ''
    for param in param_strs:
        no_space_m = param.strip()
        if not no_space_m:
            continue
        key = no_space_m[:2]
        if key in msgs:
            current_tp = msgs[key]
        elif current_tp:
            result[current_tp] = result.get(current_tp, '') + no_space_m + ' '
    return result


def get_video_url(_id):
    play_url = "http://www.94a1.com/?m=vod-play-id-%s-src-1-num-1.html" % _id
    html = extract_html("GET", play_url, None)
    search_result = pattern_down_url.search(html)
    if search_result:
        split = '$$$'
        res = search_result.group(1)
        r = unquote("'%s'" % res).replace('%', '\\')
        r = eval(r)
        name_urls = [i.split("$") for i in r.split(split)]
        name_frame_urls = [(i[0], 'https://206dy.com/vip.php?url='+i[1]) for i in name_urls]
        return name_frame_urls
    return []


def get_mvs(keyword):
    search_url = 'http://www.94a1.com/index.php?m=vod-search'
    data = {
        'wd': keyword
    }
    html = extract_html(method='POST', url=search_url, data=data)
    xhtml = etree.HTML(html)
    items = xhtml.xpath("//div[@class='stui-pannel_bd']/ul//li")
    mvs = []
    for item in items:
        temp = dict()
        temp['pic'] = get_xpath_content(item, "./div[@class='thumb']/a/@data-original")
        temp['title'] = get_xpath_content(item, "./div[@class='detail']/h3/a/text()")
        relatite_url = get_xpath_content(item, "./div[@class='detail']/h3/a/@href")
        ps = item.xpath("./div[@class='detail']//p//text()")
        brief_result = extract_mv_brief(ps)

        if relatite_url:
            temp['detail_url'] = "http://www.94a1.com" + relatite_url
            _id = get_id(temp['detail_url'])
            temp['_id'] = _id
            frame_urls = get_video_url(_id)
            temp['type_playurl'] = frame_urls
        mv_item = dict(temp, **brief_result)
        mvs.append(mv_item)
    return mvs



