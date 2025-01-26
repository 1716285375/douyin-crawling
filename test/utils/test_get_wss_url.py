from common.utils import get_wss_url, get_live_info
from pprint import pprint


def test_get_wss_url():

    url = 'https://live.douyin.com/905644984500'
    live_info = get_live_info(url)

    ids = {
        'room_id': live_info['room']['id'],
        'user_unique_id': live_info['hoster']['user_unique_uid'],
    }
    wss_url = get_wss_url(ids)
    pprint(wss_url)


if __name__ == '__main__':
    test_get_wss_url()