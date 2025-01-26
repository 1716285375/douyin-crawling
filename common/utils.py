import re
import time
import os
import json
import gzip
import hashlib
import subprocess

from loguru import logger
from pprint import pprint

import requests
import websocket
from google.protobuf import json_format
from common.types import *
from common.content import WebInfo
# from cfg.dy_pb2 import *

def get_wss_url_signature(text: str) -> str:
    """

    :param text:
    :return:
    """

    # o = r",live_id=1,aid=6383,version_code=180800,webcast_sdk_version=1.0.14-beta.0,room_id=7461032628020382514,sub_room_id=,sub_channel_id=,did_rule=3,user_unique_id=7401027138381530662,device_platform=web,device_type=,ac=,identity=audience"
    text = text[1:]
    # debug
    # logger.debug(text)

    # o_dict = json.loads(o)
    # logger.debug(o_dict)

    a = hashlib.md5(text.encode('utf-8'))

    signature = str(a.hexdigest())

    # debug
    # logger.debug(signature)

    return signature


def  get_wss_url(ids: dict[str, str]) -> str:
    """

    :param ids:
    :return:
    """
    wss_head = r'wss://webcast5-ws-web-hl.douyin.com/webcast/im/push/v2/?app_name=douyin_web'
    version_code = r'180800'
    webcast_sdk_version = r'1.0.14-beta.0'
    update_version_code = r'1.0.14-beta.0'
    compress = r'gzip'
    device_platform = r'web'
    cookie_enabled = r'true'
    screen_width = r'1920'
    screen_height = r'1080'
    browser_language = r'zh-CN'
    browser_platform = r'Win32'
    browser_name = r'Mozilla'
    browser_version = r'5.0%20(Windows%20NT%2010.0;%20Win64;%20x64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/131.0.0.0%20Safari/537.36%20Edg/131.0.0.0'
    browser_online = r'true'
    tz_name = r'Asia/Shanghai'

    # basic wss_url_head
    base_url = f"""{wss_head}&version_code={version_code}&webcast_sdk_version={webcast_sdk_version}&update_version_code={update_version_code}\
&compress={compress}&device_platform={device_platform}&cookie_enabled={cookie_enabled}&screen_width={screen_width}&screen_height={screen_height}\
&browser_language={browser_language}&browser_platform={browser_platform}&browser_name={browser_name}&browser_version={browser_version}&browser_online={browser_online}\
&tz_name={tz_name}"""

    cursor = r't-1737106925759_r-1_d-1_u-1_h-7460816982116619276'
    internal_ext = r'internal_src:dim|wss_push_room_id:7460663485614000946|wss_push_did:7387583085763151410|first_req_ms:1737106925625|fetch_time:1737106925759|seq:1|wss_info:0-1737106925759-0-0|wrds_v:7460817411055291115'
    host = r'https://live.douyin.com'
    aid = r'6383'
    live_id = r'1'
    did_rule = r'3'
    endpoint = r'live_pc'
    support_wrds = r'1'
    # user_unique_id, need to get
    user_unique_id = ids['user_unique_id']
    im_path = r'/webcast/im/fetch/'
    identity = r'audience'
    need_persist_msg_count = r'15'
    insert_task_id = r''
    live_reason = r''
    # room_id, need to get
    room_id = ids['room_id']
    heartbeatDuration = r'0'
    # signature = r'f0ob9/cJk89sxME6'

    # 计算签名
    o = f",live_id={live_id},aid={aid},version_code={version_code},webcast_sdk_version={webcast_sdk_version},room_id={room_id},sub_room_id=,sub_channel_id=,did_rule={did_rule},user_unique_id={user_unique_id},device_platform={device_platform},device_type=,ac=,identity={identity}"

    signature = subprocess.check_output(f"node ../js/sdk2.js  {get_wss_url_signature(o)}").decode('utf-8').replace('\n', '')



    suffix = f"cursor={cursor}&internal_ext={internal_ext}&host={host}&aid={aid}&live_id={live_id}\
&did_rule={did_rule}&endpoint={endpoint}&support_wrds={support_wrds}&user_unique_id={user_unique_id}\
&im_path={im_path}&identity={identity}&need_persist_msg_count={need_persist_msg_count}\
&insert_task_id={insert_task_id}&live_reason={live_reason}\
&room_id={room_id}&heartbeatDuration={heartbeatDuration}&signature={signature}"

    wss_url = base_url + suffix

    return wss_url


def get_live_info(url: str) -> dict[str, dict[str, str]]:
    """

    :param url:
    :return:
    """
    live_info = {}  # 直播间所有信息
    room = {}   # 房间信息
    hoster = {} # 主播信息
    web = {}    # url信息
    stream = {} # 直播流信息

    # 请求头
    web_info = WebInfo()
    headers = web_info.headers
    cookies = web_info.cookies
    # 获取html数据
    response = requests.get(url, headers=headers, cookies=cookies)
    response.encoding = 'utf-8'

    # 响应状态
    if response.status_code == 200:
        # debug
        # logger.debug(f"web信息 >>> ttwid <<<是: {web['ttwid']}")

        cookies = response.cookies.get_dict()
        web['ttwid'] = cookies['ttwid']
        # debug
        # logger.debug(f"web信息 >>> ttwid <<<是: {web['ttwid']}")

        res = response.text

        with open('./live_info.txt', 'w', encoding='utf-8') as f:
            f.write(res)


        # 获取网页信息
        # data_string = re.findall(r'<script nonce=".*?" >self.__pace_f.push\(\[1,"d:(.*?)\\n"\]\)</script>', res)[0]
        # data_string = re.findall(r'<script nonce>self.__pace_f.push\(\[1,"\{\\"common\\":\{(.*?)"\]\)</script>', res)[0]
        # data_dict = json.loads(data_string.replace('\\"', '"').replace('\\u0026', '&').replace('\\"', '"'))
        # pprint(data_dict)

        # 获取直播房间信息
        room['id'] = re.findall(r'\\"roomId\\":\\"(\d+)\\"', res)[0]

        # >>> debug
        # logger.debug(room['id'])

        # 获取主播信息
        hoster['user_unique_uid'] = re.search(r'\\"user_unique_id\\":\\"(\d+)\\"', res).group(1)
        if hoster['user_unique_uid'] is not None:
            hoster['user_unique_uid'] = hoster['user_unique_uid']

        # >>> debug
        # logger.debug(hoster['user_unique_uid'])

    else:
        logger.error(f"error: {requests.exceptions.ConnectionError} \t status_code: {response.status_code}")
        raise requests.exceptions.RequestException

    live_info['hoster'] = hoster
    live_info['room'] = room
    live_info['web'] = web
    live_info['stream'] = stream

    return live_info

# -----------------------------------------------------------------------------------
# old version, it's too tedious to get the live info
def old_get_live_info(url: str) -> dict[str, dict[str, str]]:
    """

    :param url:
    :return: 直播信息, 包含直播房间信息, 主播信息
    room: {
        id:
        status:
        title:
    }
    """
    live_info = {}  # 直播间所有信息
    room = {}   # 房间信息
    hoster = {} # 主播信息
    web = {}    # url信息
    stream = {} # 直播流信息

    # 请求头
    web_info = WebInfo()
    headers = web_info.headers
    cookies = web_info.cookies
    # 获取html数据
    response = requests.get(url, headers=headers, cookies=cookies)
    response.encoding = 'utf-8'

    # 响应状态
    if response.status_code == 200:

        # debug
        # logger.debug(f"web信息 >>> ttwid <<<是: {web['ttwid']}")

        cookies = response.cookies.get_dict()
        web['ttwid'] = cookies['ttwid']
        # debug
        # logger.debug(f"web信息 >>> ttwid <<<是: {web['ttwid']}")

        res = response.text

        # 获取直播房间信息
        data_string = re.findall(r'<script nonce=".*?" >self.__pace_f.push\(\[1,"d:(.*?)\\n"\]\)</script>', res)[0]
        data_dict = json.loads(data_string.replace('\\"', '"').replace('\\u0026', '&').replace('\\"', '"'))
        pprint(data_dict[3]['state']['roomStore']['roomInfo']['roomId'])
        room_info = re.search(r'room\\":{.*\\"id_str\\":\\"(\d+)\\".*,\\"status\\":(\d+).*,\\"title\\":\\"([^"]*)\\"', res)
        if room_info is not None:
            room['id'] = re.search(r'roomId\\":\\"(\d+)\\"', res).group(1)
            room['title'] = room_info.group(3)
            room['status'] = room_info.group(2)

            if room['status'] == '4':
                logger.error("Connection-Error: 直播已经结束")
                raise ConnectionError("直播已结束")
                # raise ConnectionError(logger.error("直播已结束"))
            # debug
            # logger.debug(f"直播房间信息是: {room}")

        # 获取主播信息
        user_unique_id = re.search(r'\\"user_unique_id\\":\\"(\d+)\\"', res).group(1)
        if user_unique_id is not None:
            hoster['user_unique_uid'] = user_unique_id

        # 获取直播流数据
        stream_m3u8_info = re.search(r'"hls_pull_url_map\\":(\{.*?})', res)
        if stream_m3u8_info is not None:
            stream['m3u8'] = json.loads(stream_m3u8_info.group(1).replace('\\"', '"'))
            # debug
            # logger.debug(f"直播流m3u8的链接地址是: {stream['m3u8']}")

        stream_flv_info = re.search(r'flv\\":\\"(.*?)\\"', res)
        # debug
        # logger.debug(stream_flv_info.group(1))
        if stream_flv_info is not None:
            stream['flv'] = stream_flv_info.group(1).replace('\\"', '"').replace("\\u0026", "&")
            if "https" not in stream['flv']:
                stream['flv'] = stream['flv'].replace("http", "https")
                # debug
                # logger.debug(f"直播流flv的链接地址是: {stream['flv']}")
    else:
        logger.error(f"error: {requests.exceptions.ConnectionError} \t status_code: {response.status_code}")

    live_info['room'] = room
    live_info['hoster'] = hoster
    live_info['web'] = web
    live_info['stream'] = stream

    # pprint(live)

    return live_info
# -----------------------------------------------------------------------------------

def get_live_room_danmaku(live: dict[str, dict[str, str]]):
    pass


# def get_wss_url(live: dict[str, dict[str, str]]) -> str:
#
#     pass