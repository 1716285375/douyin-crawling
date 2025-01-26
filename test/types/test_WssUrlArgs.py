from common.types import WwsUrlArgs
from pprint import pprint


def test_WssUrlArgs():
    wws_url_args = WwsUrlArgs()
    pprint(wws_url_args.params)


if __name__ == '__main__':
    test_WssUrlArgs()