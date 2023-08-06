class UserInfo:
    def __init__(self, name: str, headImgUrl: str, openId: str, unionId: str, token: str) -> None:
        """用户信息

        登录时获取到的用户信息，皆与微信有关
        :param: name: 微信名
        :param: headImgUrl: 头像链接
        :param: openId: 微信认证参数
        :param: unionId: 微信认证参数
        """
        self.name = name
        self.headImgUrl = headImgUrl
        self.openId = openId
        self.unionId = unionId
        self.token = token

    def __str__(self) -> str:
        return f"name: {self.name}, headImgUrl: {self.headImgUrl}, openId: {self.openId}, unionId: {self.unionId}, token: {self.token}"

    def __repr__(self) -> str:
        return f"<UserInfo: {self.name}, headImgUrl: {self.headImgUrl}, openId: {self.openId}, unionId: {self.unionId}, token: {self.token}>"


class CourseInfo:
    def __init__(self, _id: int, subId: int, title: str, intro: str, level: int, price: float, expired: bool) -> None:
        self._id = _id
        self.subId = subId
        self.title = title
        self.intro = intro
        self.level = level
        self.price = price
        self.expired = expired
