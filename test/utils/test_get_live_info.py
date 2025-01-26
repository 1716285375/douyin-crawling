from common.utils import get_live_info
from pprint import pprint


def test_get_live_info():
    url = 'https://live.douyin.com/751040752420'
    live = get_live_info(url)
    # pprint(live)


if __name__ == '__main__':
    test_get_live_info()