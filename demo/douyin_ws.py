from websocket import WebSocketApp
import json
import re
import gzip
from urllib.parse import unquote_plus
import requests
import pprint
from loguru import logger
from cfg.v2_pb2 import PushFrame, Response, ChatMessage
from common.utils import get_live_info, get_wss_url


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    "Cookie": "__ac_nonce=0678209320057551b22a7; __ac_signature=_02B4Z6wo00f01AA3nBAAAIDANxNYTy9XgxgAF5iAAGeW2f; ttwid=1%7Cg8sF8W4rwtl3glMZcA9yIYw2drk_7NrGqsFIRNfOlJw%7C1736575282%7C25ab5934855dcfc6e144992091aea71ce54eb53bc562e0ef28941f4ef7fb618c; x-web-secsdk-uid=06090e1b-d7ab-4ca1-a364-4feb17a64b41; __live_version__=%221.1.2.6953%22; has_avx2=null; device_web_cpu_core=20; device_web_memory_size=8; live_use_vvc=%22false%22; hevc_supported=true; xgplayer_user_id=519156810381; csrf_session_id=40520d7408a6890d81bcf57c233fd8d2; h265ErrorNum=-1; webcast_local_quality=sd; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; fpk1=U2FsdGVkX19hC9JWq93Jum0pQECCARo8O5utefLKfS5c4cMO+THgyg/tI+3waVg+Ha8Xg/A4JfUUkQvXy8VBQg==; fpk2=ffc3218438300d069a0fd5dfa5c6e851; xg_device_score=7.77828219547939; live_can_add_dy_2_desktop=%221%22; download_guide=%221%2F20250111%2F0%22; IsDouyinActive=false"
}


def fetch_live_room_info(url):
    live = get_live_info(url)

    room_id = live['room']['id']
    room_title = 'title'
    ttwid = live['web']['ttwid']
    user_unique_id = live['hoster']['user_unique_uid']
    room_user_count = r'9000'
    ids = {
        'room_id': room_id,
        'user_unique_id': user_unique_id
    }
    wss_url = get_wss_url(ids)

    # debug
    # logger.debug(wss_url)

    return room_id, room_title, room_user_count, wss_url, ttwid


def on_open(ws, content):
    logger.debug("open")


def on_message(ws, content):
    frame = PushFrame()
    # 获取接收的content字节数据，存储到frame中
    frame.ParseFromString(content)

    # 对PushFrame的 payload 内容进行gzip解压
    origin_bytes = gzip.decompress(frame.payload)

    # 根据Response+gzip解压数据，生成数据对象
    response = Response()
    response.ParseFromString(origin_bytes)

    if response.needAck:
        s = PushFrame()
        s.payloadType = "ack"
        s.payload = response.internalExt.encode('utf-8')
        s.logId = frame.logId
        ws.send(s.SerializeToString())

    # 获取数据内容（需根据不同method，使用不同的结构对象对 数据 进行解析）
    #   注意：此处只处理 WebcastChatMessage ，其他处理方式都是类似的。

    # print(response.messagesList.method)
    for item in response.messagesList:
        if item.method != "WebcastChatMessage":
            continue
        message = ChatMessage()
        message.ParseFromString(item.payload)
        info = f"【Lv{message.user.Level}-{message.user.nickName}】: \"{message.content}\" "
        logger.info(info)


def on_error(ws, content):
    # print("on_error")
    logger.error("on_error")


def on_close(ws, content):
    # print("on_close")
    logger.debug("on_close")


def run():
    web_url = "https://live.douyin.com/905644984500"

    room_id, room_title, room_user_count, wss_url, ttwid = fetch_live_room_info(web_url)
    ws = WebSocketApp(
        url=wss_url,
        header={},
        cookie=f"ttwid={ttwid}",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.run_forever()


if __name__ == '__main__':
    run()
