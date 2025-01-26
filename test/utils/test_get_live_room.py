import json
import re
from urllib.parse import unquote_plus
import requests

res = requests.get(
    url="https://live.douyin.com/80017709309",
    headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    },
    cookies={
        "__ac_nonce": "063abcffa00ed8507d599"  # 可以是任意值
    }
)
data_string = re.findall(r'<script id="RENDER_DATA" type="application/json">(.*?)</script>', res.text)[0]
data_dict = json.loads(unquote_plus(data_string))

room_id = data_dict['app']['initialState']['roomStore']['roomInfo']['roomId']
room_title = data_dict['app']['initialState']['roomStore']['roomInfo']["room"]['title']
room_user_count = data_dict['app']['initialState']['roomStore']['roomInfo']["room"]['user_count_str']

print(room_title, room_user_count)
print(room_id)