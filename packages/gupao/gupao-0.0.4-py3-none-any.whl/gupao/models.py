class LoginInfo:
    def __init__(self, name: str, headImgUrl: str, openId: str, unionId: str) -> None:
        """登录信息

        登录时获取到的用户信息，皆与微信有关
        :param: name: 微信名
        :param: headImgUrl: 头像链接
        :param: openId: 微信认证参数
        :param: unioonId: 微信认证参数
        """
        self.name = name
        self.headImgUrl = headImgUrl
        self.openId = openId
        self.unionId = unionId

    def __str__(self) -> str:
        return f"name: {self.name}; headImgUrl: {self.headImgUrl}; openId: {self.openId}; unionId: {self.unionId};"
