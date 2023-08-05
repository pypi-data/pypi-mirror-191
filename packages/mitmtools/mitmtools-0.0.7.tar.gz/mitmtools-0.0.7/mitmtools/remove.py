"""
    内容去除

    提供以下方法：
        RemoveContent：通过正则匹配 url，并去除部分响应内容
"""
from typing import List
from mitmproxy import http
from mitmtools.base import MitmproxyBase


class RemoveBase(MitmproxyBase):
    def __init__(self, pattern: str, remove_list: List[str], max_times: int = None, **kwargs):
        """

        :param pattern: 正则匹配 url
        :param remove_list: 移除列表
        :param max_times: 匹配次数，默认无限匹配
        """
        super().__init__(**kwargs)
        self.pattern = pattern
        self.remove_list = remove_list
        self.max_times = max_times
        self.remove_times = 0  # 移除的次数
        self.kwargs = kwargs
        self.kwargs.setdefault("flags", 0)  # 正则的 flags

    def add_times(self):
        """
        匹配次数 +1

        :return:
        """
        if self.max_times:
            self.remove_times += 1

    @property
    def is_end(self) -> bool:
        """
        是否到最大次数了

        :return:
        """
        if self.max_times and self.remove_times >= self.max_times:
            return True

        return False


class RemoveContent(RemoveBase):
    """
        移除指定内容
    """

    def __init__(self, pattern: str, remove_list: List[str], max_times: int = None, **kwargs):
        """
        取值响应的指定内容

        :param pattern: 正则匹配 url
        :param remove_list: 移除列表
        :param max_times: 匹配次数，默认无限匹配
        """
        super().__init__(pattern, remove_list, max_times, **kwargs)

    def response(self, flow: http.HTTPFlow) -> None:
        """
        遍历替换响应内容

        :param flow:
        :return:
        """
        if self.is_match(self.pattern, flow.request.url, self.kwargs["flags"]) and not self.is_end:
            self.add_times()

            for r in self.remove_list:
                encoding = self.get_encoding(flow)
                flow.response.content = flow.response.content.replace(r.encode(encoding), b'')
