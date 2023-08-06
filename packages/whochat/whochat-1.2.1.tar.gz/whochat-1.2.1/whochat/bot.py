import functools
import json
import os
import pathlib
import shutil
import tempfile
import threading
from datetime import datetime
from typing import Dict, List, Union

import psutil

from ._comtypes import client as com_client
from .abc import CWechatRobotABC, RobotEventABC, RobotEventSinkABC
from .logger import logger
from .utils import guess_wechat_user_by_paths

_robot_local = threading.local()


# 保证每个线程的COM对象独立
def get_robot_object(com_id) -> CWechatRobotABC:
    if not hasattr(_robot_local, "robot_object"):
        setattr(_robot_local, "robot_object", com_client.CreateObject(com_id))
    return getattr(_robot_local, "robot_object")


def get_robot_event(com_id) -> RobotEventABC:
    if not hasattr(_robot_local, "robot_event"):
        setattr(_robot_local, "robot_event", com_client.CreateObject(com_id))
    return getattr(_robot_local, "robot_event")


def auto_start(func):
    @functools.wraps(func)
    def wrapper(self: "WechatBot", *args, **kwargs):
        self.start_robot_service()
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            logger.exception(e)

    return wrapper


class WechatBot:
    def __init__(self, wx_pid, robot_object_id: str, robot_event_id: str = None):
        self.wx_pid = int(wx_pid)
        self._robot_object_id = robot_object_id
        self._robot_event_id = robot_event_id
        self.started = False
        self.user_info = {}
        self.event_connection = None

    @property
    def robot(self):
        return get_robot_object(self._robot_object_id)

    @property
    def robot_event(self):
        return get_robot_event(self._robot_event_id)

    def __enter__(self):
        self.start_robot_service()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_robot_service()

    def start_robot_service(self):
        if self.started:
            return True
        result = self.robot.CStartRobotService(
            self.wx_pid,
        )
        if result == 0:
            self.started = True
        return not result

    def stop_robot_service(self):
        if not self.started:
            return True
        result = self.robot.CStopRobotService(
            self.wx_pid,
        )
        if result == 0:
            self.started = False
        return not result

    @auto_start
    def send_image(self, wx_id, img_path):
        abs_path = pathlib.Path(img_path).absolute()
        # BUG: (20220821)图片文件名如果有多个"."的话不能成功发送, 所以复制到临时文件进行发送
        if "." in abs_path.stem:
            with tempfile.TemporaryDirectory() as td:
                temp_path = os.path.join(td, os.urandom(5).hex() + abs_path.suffix)
                shutil.copy(abs_path, temp_path)
                return self.robot.CSendImage(self.wx_pid, wx_id, temp_path)

        return self.robot.CSendImage(self.wx_pid, wx_id, str(abs_path))

    @auto_start
    def send_text(self, wx_id, text):
        return self.robot.CSendText(self.wx_pid, wx_id, text)

    @auto_start
    def send_file(self, wx_id, filepath):
        abs_path = pathlib.Path(filepath).absolute()
        return self.robot.CSendFile(self.wx_pid, wx_id, str(abs_path))

    @auto_start
    def send_article(
        self, wxid: str, title: str, abstract: str, url: str, imgpath: str
    ):
        return self.robot.CSendArticle(self.wx_pid, wxid, title, abstract, url, imgpath)

    @auto_start
    def send_card(self, wxid: str, shared_wxid: str, nickname: str):
        return self.robot.CSendCard(self.wx_pid, wxid, shared_wxid, nickname)

    @auto_start
    def send_at_text(
        self,
        chatroom_id: str,
        at_wxids: Union[str, List[str]],
        text: str,
        auto_nickname: bool = True,
    ):
        return self.robot.CSendAtText(
            self.wx_pid, chatroom_id, at_wxids, text, auto_nickname
        )

    @auto_start
    def get_friend_list(self):
        return [
            dict(item)
            for item in (
                self.robot.CGetFriendList(
                    self.wx_pid,
                )
                or []
            )
        ]

    @auto_start
    def get_wx_user_info(self, wxid: str):
        return json.loads(self.robot.CGetWxUserInfo(self.wx_pid, wxid))

    @auto_start
    def get_self_info(self, refresh=False):
        if refresh or not self.user_info:
            self.user_info = json.loads(
                self.robot.CGetSelfInfo(
                    self.wx_pid,
                )
            )
        return self.user_info

    @auto_start
    def check_friend_status(self, wxid: str):
        return self.robot.CCheckFriendStatus(self.wx_pid, wxid)

    @auto_start
    def get_com_work_path(self):
        return self.robot.CGetComWorkPath(
            self.wx_pid,
        )

    @auto_start
    def start_receive_message(self, port: int):
        """
        开始接收消息
        :param port: 端口， port为0则使用COM Event推送
        """
        return self.robot.CStartReceiveMessage(self.wx_pid, port)

    @auto_start
    def stop_receive_message(self):
        return self.robot.CStopReceiveMessage(
            self.wx_pid,
        )

    @auto_start
    def get_chat_room_member_ids(self, chatroom_id: str):
        wx_ids_str: str = self.robot.CGetChatRoomMembers(self.wx_pid, chatroom_id)[1][1]
        wx_ids = wx_ids_str.split("^G")
        return wx_ids

    @auto_start
    def get_chat_room_member_nickname(self, chatroom_id: str, wxid: str):
        return self.robot.CGetChatRoomMemberNickname(self.wx_pid, chatroom_id, wxid)

    def get_chat_room_members(self, chatroom_id: str) -> List[dict]:
        """
        获取群成员id及昵称信息

        [
            {
                "wx_id": "",
                "nickname": ""
            }
        ]
        """
        results = []
        for wx_id in self.get_chat_room_member_ids(chatroom_id):
            results.append(
                {
                    "wx_id": wx_id,
                    "nickname": self.get_chat_room_member_nickname(chatroom_id, wx_id),
                }
            )
        return results

    @auto_start
    def add_friend_by_wxid(self, wxid: str, message: str):
        return self.robot.CAddFriendByWxid(self.wx_pid, wxid, message)

    @auto_start
    def search_contact_by_net(self, keyword: str):
        return [
            dict(item) for item in self.robot.CSearchContactByNet(self.wx_pid, keyword)
        ]

    @auto_start
    def add_brand_contact(self, public_id: str):
        return self.robot.CAddBrandContact(self.wx_pid, public_id)

    @auto_start
    def change_we_chat_ver(self, version: str):
        return self.robot.CChangeWeChatVer(self.wx_pid, version)

    @auto_start
    def send_app_msg(self, wxid: str, app_id: str):
        return self.robot.CSendAppMsg(self.wx_pid, wxid, app_id)

    @auto_start
    def delete_user(self, wxid: str):
        return self.robot.CDeleteUser(self.wx_pid, wxid)

    @auto_start
    def is_wx_login(self) -> int:
        return self.robot.CIsWxLogin(
            self.wx_pid,
        )

    @auto_start
    def get_db_handles(self):
        return [dict(item) for item in self.robot.CGetDbHandles(self.wx_pid)]

    @auto_start
    def register_event(self, event_sink: RobotEventSinkABC):
        if self.event_connection:
            self.event_connection.__del__()
        self.event_connection = com_client.GetEvents(self.robot_event, event_sink)
        self.robot_event.CRegisterWxPidWithCookie(
            self.wx_pid, self.event_connection.cookie
        )

    @auto_start
    def get_we_chat_ver(self) -> str:
        return self.robot.CGetWeChatVer()

    @auto_start
    def hook_voice_msg(self, savepath: str) -> int:
        return self.robot.CHookVoiceMsg(self.wx_pid, savepath)

    @auto_start
    def unhook_voice_msg(self):
        return self.robot.CUnHookVoiceMsg(self.wx_pid)

    @auto_start
    def hook_image_msg(self, savepath: str) -> int:
        return self.robot.CHookImageMsg(self.wx_pid, savepath)

    @auto_start
    def unhook_image_msg(self):
        return self.robot.CUnHookImageMsg(self.wx_pid)

    @auto_start
    def open_browser(self, url: str):
        return self.robot.COpenBrowser(self.wx_pid, url)

    @auto_start
    def get_history_public_msg(self, public_id: str, offset: str = ""):
        """
        获取公众号历史消息

        Args:
            offset (str, optional): 起始偏移，为空的话则从新到久获取十条，该值可从返回数据中取得
        """
        r = self.robot.CGetHistoryPublicMsg(self.wx_pid, public_id, offset)
        try:
            msgs = json.loads(r[0])
        except (IndexError, json.JSONDecodeError) as e:
            logger.exception(e)
            return []
        return msgs

    @auto_start
    def forward_message(self, wxid: str, msgid: int):
        """
        转发消息

        Args:
            wxid (str): 消息接收人
            msgid (int): 消息id
        """
        return self.robot.CForwardMessage(self.wx_pid, wxid, msgid)

    @auto_start
    def get_qrcode_image(
        self,
    ) -> bytes:
        """
        获取二维码，同时切换到扫码登陆

        Returns:
            bytes
                二维码bytes数据.
        You can convert it to image object,like this:
        >>> from io import BytesIO
        >>> from PIL import Image
        >>> buf = wx.GetQrcodeImage()
        >>> image = Image.open(BytesIO(buf)).convert("L")
        >>> image.save('./qrcode.png')
        """
        return self.robot.CGetQrcodeImage(self.wx_pid)

    @auto_start
    def get_a8_key(self, url: str):
        """
        获取A8Key

        Args:
            url (str): 公众号文章链接
        """
        r = self.robot.CGetA8Key(self.wx_pid, url)
        try:
            result = json.loads(r[0])
        except (IndexError, json.JSONDecodeError) as e:
            logger.exception(e)
            return ""
        return result

    @auto_start
    def send_xml_msg(self, wxid: str, xml: str, img_path: str) -> int:
        """
        发送原始xml消息

        Returns:
            int: 0表示成功
        """
        return self.robot.CSendXmlMsg(self.wx_pid, wxid, xml, img_path)

    @auto_start
    def logout(self) -> int:
        """
        登出

        Returns:
            int: 0表示成功
        """
        return self.robot.CLogout(self.wx_pid)

    @auto_start
    def get_transfer(self, wxid: str, transactionid: str, transferid: int) -> int:
        """
        收款

        Args:
            wxid : str
                转账人wxid.
            transcationid : str
                从转账消息xml中获取.
            transferid : str
                从转账消息xml中获取.

        Returns:
            int
                成功返回0，失败返回非0值.
        """
        return self.robot.CGetTransfer(self.wx_pid, wxid, transactionid, transferid)

    @auto_start
    def send_emotion(self, wxid: str, img_path: str) -> int:
        return self.robot.CSendEmotion(self.wx_pid, wxid, img_path)

    @auto_start
    def get_msg_cdn(self, msgid: int) -> str:
        """
        下载图片、视频、文件等

        Returns:
            str
                成功返回文件路径，失败返回空字符串.
        """
        return self.robot.CGetMsgCDN(self.wx_pid, msgid)


class WechatBotFactoryMetaclass(type):
    _robot: CWechatRobotABC
    _robot_object_id: str
    _robot_event_id: str

    @property
    def robot(cls):
        return get_robot_object(cls._robot_object_id)

    @property
    def robot_event(cls):
        return get_robot_event(cls._robot_event_id)

    @property
    def robot_pid(cls) -> int:
        return cls.robot.CStopRobotService(0)


class WechatBotFactory(metaclass=WechatBotFactoryMetaclass):
    """
    单例
    """

    _instances: Dict[int, "WechatBot"] = {}
    _robot_object_id = "WeChatRobot.CWeChatRobot"
    _robot_event_id = "WeChatRobot.RobotEvent"

    @classmethod
    def get(cls, wx_pid) -> "WechatBot":
        if wx_pid not in cls._instances:
            cls._instances[wx_pid] = WechatBot(
                wx_pid, cls._robot_object_id, cls._robot_event_id
            )
        return cls._instances[wx_pid]

    @classmethod
    def exit(cls):
        logger.info("卸载注入的dll...")
        for instance in cls._instances.values():
            instance.stop_robot_service()

    @classmethod
    def get_we_chat_ver(cls) -> str:
        return cls.robot.CGetWeChatVer()

    @classmethod
    def start_wechat(cls) -> int:
        return cls.robot.CStartWeChat()

    @classmethod
    def list_wechat(cls) -> List[dict]:
        results = []
        for process in psutil.process_iter():
            if process.name().lower() == "wechat.exe":
                files = [f.path for f in process.open_files()]
                results.append(
                    {
                        "pid": process.pid,
                        "started": datetime.fromtimestamp(process.create_time()),
                        "status": process.status(),
                        "wechat_user": guess_wechat_user_by_paths(files),
                    }
                )
        return results

    @classmethod
    def get_robot_pid(cls):
        return cls.robot_pid

    @classmethod
    def kill_robot(cls):
        bot_pid = cls.robot_pid
        logger.info(f"尝试结束CWeChatRobot进程: pid {bot_pid}")
        try:
            psutil.Process(bot_pid).kill()
            logger.info("OK")
        except psutil.Error as e:
            logger.warning(e, exc_info=True)

    @classmethod
    def register_events(cls, wx_pids, event_sink: RobotEventSinkABC):
        connection = com_client.GetEvents(cls.robot_event, event_sink)
        for wx_pid in wx_pids:
            cls.robot_event.CRegisterWxPidWithCookie(wx_pid, connection.cookie)
