"""
    根据 url 替换指定响应内容

    提供以下方法：
        ReplaceByFile：通过正则匹配 url，使用文件替换整个响应
        ReplaceByStr：通过正则匹配 url，使用字典替换部分字段
"""
from typing import Dict
from loguru import logger
from mitmproxy import http
from mitmtools.base import MitmproxyBase


class ReplaceBase(MitmproxyBase):

    def __init__(self, pattern: str, max_times: int = None, **kwargs):
        """

        :param pattern: 匹配规则 url
        :param filepath: 从文件替换
        :param content: 从字符串替换
        :param max_times: 匹配次数，默认无限匹配
        """
        super().__init__(**kwargs)
        self.pattern = pattern
        self.max_times = max_times
        self.replace_times = 0  # 替换的次数
        self.kwargs = kwargs
        self.kwargs.setdefault("flags", 0)  # 正则的 flags

    def add_times(self):
        """
        匹配次数 +1

        :return:
        """
        if self.max_times:
            self.replace_times += 1

    @property
    def is_end(self) -> bool:
        """
        是否到最大次数了

        :return:
        """
        if self.max_times and self.replace_times >= self.max_times:
            return True

        return False


class ReplaceByFile(ReplaceBase):
    """
        通过文件替换全部响应内容
    """

    def __init__(self, pattern: str, filepath: str, max_times: int = None, **kwargs):
        """

        :param pattern: 正则匹配 url
        :param filepath: 文件路径
        :param max_times: 匹配次数，默认无限匹配
        """
        super().__init__(pattern, max_times, **kwargs)
        self.filepath = filepath

    def response(self, flow: http.HTTPFlow) -> None:
        """
        响应，拦截替换文件

        :param flow:
        :return:
        """
        self.show_response_detail(flow)

        if self.is_match(self.pattern, flow.request.url, self.kwargs["flags"]) and not self.is_end:
            self.add_times()

            flow.response.content = self.load_file(filepath=self.filepath, byte=True)
            logger.debug(f"{flow.request.url} 已替换文件：{self.filepath}")


class ReplaceByStr(ReplaceBase):
    """
        通过字符串替换指定响应内容的部分内容
    """

    def __init__(self, pattern: str, replace_dict: Dict[str, str], max_times: int = None, **kwargs):
        """
        通过 url 的完全匹配 替换响应

        :param pattern: 正则匹配 url
        :param replace_dict: 替换的字典
        :param max_times: 匹配次数，默认无限匹配
        """
        super().__init__(pattern, max_times, **kwargs)
        self.replace_dict = replace_dict

    def response(self, flow: http.HTTPFlow) -> None:
        """
        响应，拦截替换文件

        :param flow:
        :return:
        """
        self.show_response_detail(flow)

        if self.is_match(self.pattern, flow.request.url, self.kwargs["flags"]) and not self.is_end:
            self.add_times()

            encoding = self.get_encoding(flow)

            for key, value in self.replace_dict.items():
                flow.response.content = flow.response.content.replace(
                    key.encode(encoding),
                    value.encode(encoding)
                )
                logger.debug(f"{flow.request.url} 已替换响应：{key} -> {value}")
