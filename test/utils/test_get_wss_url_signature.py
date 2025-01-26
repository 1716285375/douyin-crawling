from common.utils import  get_wss_url_signature


def test_get_wss_url_signature():
    a = get_wss_url_signature('s')
    if a == r"7d0a09acfd21d6a24ffa0f464f0aa78e":
        print(f">>> equal")
    else:
        print(f">>> not equal")
    pass


if __name__ == '__main__':
    test_get_wss_url_signature()