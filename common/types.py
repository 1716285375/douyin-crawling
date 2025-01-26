from cfg.dy_pb2 import *


"""
dy_pb2 includes some classes as follows:
------------------------
PushFrame
Response
MatchAgainstScoreMessage
LikeMessage
MemberMessage
GiftMessage
ChatMessage
SocialMessage
RoomUserSeqMessage
UpdateFanTicketMessage
CommonTextMessage
ProductChangeMessage
------------------------
"""


class WwsUrlArgs:
    """
    wws_url的参数
    """
    def __init__(self,
                 room_id: str = None,
                 signature: str = None,):
        self._params = {
            'app_name': 'douyin_web',
            'version_code': '180800',
            'webcast_sdk_version': '1.0.14-beta.0',
            'update_version_code': '1.0.14-beta.0',
            'compress': 'gzip',
            'device_platform': 'web',
            'cookie_enabled': 'true',
            'screen_width': '1920',
            'screen_height': '1080',
            'browser_language': 'zh-CN',
            'browser_platform': 'Win32',
            'browser_name': 'Mozilla',
            'browser_version': '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            'browser_online': 'true',
            'tz_name': 'Asia/Shanghai',
            'cursor': 't-1737127541184_r-1_d-1_u-1_h-7460905900120691738',
            'internal_ext': f'internal_src:dim|wss_push_room_id:{room_id}|wss_push_did:7401027138381530662|first_req_ms:1737127541078|fetch_time:1737127541184|seq:1|wss_info:0-1737127541184-0-0|wrds_v:7460905951806101238',
            'host': 'https://live.douyin.com',
            'aid': '6383',
            'live_id': '1',
            'did_rule': '3',
            'endpoint': 'live_pc',
            'support_wrds': '1',
            'user_unique_id': '7401027138381530662',
            'im_path': '/webcast/im/fetch/',
            'identity': 'audience',
            'need_persist_msg_count': '15',
            'insert_task_id': '',
            'live_reason': '',
            'room_id': room_id,
            'heartbeatDuration': '0',
            'signature': signature,
        }

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, value):
        if not isinstance(value, dict):
            raise TypeError('param must be a dict')
        self._params = value