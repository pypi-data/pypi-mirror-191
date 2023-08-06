import requests
import time
from typing import Tuple, Optional
from . import apis
from .models import *
import webbrowser


class GuPao:
    def __init__(self) -> None:
        """咕泡云课堂接口
        """
        self.__client: requests.Session = requests.Session()
        self.__timeout: int = 5

    def __checker(func):
        """检查是否登录
        """

        def ware(self, *args, **kwargs):
            if not hasattr(self, "loginInfo"):
                raise Exception(
                    'You should login before call "' + func.__name__ + '"')
            return func(self, *args, **kwargs)
        return ware

    def Login(self, auto_open=True, output=True) -> Optional[LoginInfo]:
        """登录

        对扫码登录一系列动作的封装，包括获取二维码信息、指引用户扫码登录、轮询获取登录信息。当然你也可以仿照该逻辑自定义登录方法。
        :param: auto_open: 是否自动在浏览器打开二维码链接，默认`是`
        :param: output: 是否在控制台打印二维码链接，默认`是`
        """
        codeUrl, ticket = self.getLoginQRCode()
        if output:
            print(
                "==>\033[1;34m Please scan the code with wechat to login.\033[0m")
            print("==>\033[1;34m Login QRCode URL: " + codeUrl + "\033[0m")
        if auto_open:
            if webbrowser.open(codeUrl):
                print(
                    "==>\033[1;34m The code has been opened with your default browser.\033[0m")
            else:
                print(
                    "==>\033[1;31m Open code url with browser failed, maybe you can open it by your self.\033[0m")
        index: int = 0
        while (index := index+3) <= 60:
            time.sleep(3)
            if info := self.checkLoginStatus(ticket):
                return info
        return Exception("The QR code seems to be out of date.")

    def setTimeout(self, value: int) -> None:
        """设置全局请求超时，默认超时为8秒

        :param: value: 超时时长，单位（秒）
        """
        self.__timeout = value

    def getLoginQRCode(self) -> Tuple[str, str]:
        """获取登录二维码

        :returns: codeUrl: 二维码图片链接
        :returns: ticket: 二维码标识
        """
        response: requests.Response = self.__client.get(
            apis.URL_AUTHQRCODE, timeout=self.__timeout)
        if response.status_code == 200 and response.json().get('code') == 0 and (data := response.json().get('data')):
            return data.get('codeUrl'), data.get('ticket')
        raise Exception("getLoginUrl error! ")

    def checkLoginStatus(self, ticket: str) -> Optional[LoginInfo]:
        """检查登录状态

        轮询该方法以判断用户是否成功扫码登录，注意轮询间隔应不小于3秒，预计过期时间为一分钟
        :param: ticket: 二维码标识，通过`getLoginQRCode`方法获取
        :returns: userInfo: 成功返回用户信息，失败返回None
        """
        url: str = f"{apis.URL_CHECKLOGIN}?ticket={ticket}"
        response: requests.Response = self.__client.get(
            url, timeout=self.__timeout)
        if response.status_code == 200 and response.json().get('code') == 0 and (data := response.json().get('data')):
            if data.get('code') != 0:
                return None
            self.loginInfo = LoginInfo(**data.get('data'))
            return self.loginInfo
        raise Exception("checkLoginStatus error! ")