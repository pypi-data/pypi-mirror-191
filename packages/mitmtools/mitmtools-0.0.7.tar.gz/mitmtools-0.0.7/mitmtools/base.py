"""
    所有的程序主体结构
"""
import re
import chardet
from typing import Union
from mitmproxy import http
from mitmtools.log import Logger
from urllib.parse import urlparse
from print_dict import format_dict


class MitmproxyBase:

    def __init__(self, encoding: str = 'utf-8'):
        self.logger = Logger()
        self.encoding = encoding

    def request(self, flow: http.HTTPFlow) -> None:
        """
        请求发起之前处理

        :param flow:
        :return:
        """

    def response(self, flow: http.HTTPFlow) -> None:
        """
        响应发送之前处理

        :param flow:
        :return:
        """

    @staticmethod
    def parse_request_headers(flow: http.HTTPFlow) -> dict:
        return dict(flow.request.headers)

    @staticmethod
    def parse_request_params(flow: http.HTTPFlow) -> dict:
        return dict(flow.request.query)

    @staticmethod
    def parse_request_cookie(flow: http.HTTPFlow) -> dict:
        if isinstance(flow.request.cookies, list):
            return dict(flow.request.cookies)
        else:
            return dict([(c[0], c[1]) for c in flow.request.cookies.fields])

    @staticmethod
    def parse_response_headers(flow: http.HTTPFlow) -> dict:
        return dict(flow.response.headers)

    @staticmethod
    def parse_response_cookie(flow: http.HTTPFlow) -> dict:
        if isinstance(flow.response.cookies, list):
            return dict(flow.response.cookies)
        else:
            return dict([(c[0], c[1]) for c in flow.request.cookies.fields])

    def show_request_detail(self, flow: http.HTTPFlow) -> None:
        """
        显示请求的详情字符串

        :return:
        """
        lines = [
            f'\n********** Request {flow.request.method} {flow.request.url}  **********',
            f'http_version: {flow.request.http_version}',
            f'headers: {format_dict(self.parse_request_headers(flow))}',
            f'params: {format_dict(self.parse_request_params(flow))}',
            f'cookie：{format_dict(self.parse_request_cookie(flow))}'
        ]
        self.logger.debug('\n'.join(lines))

    def show_response_detail(self, flow: http.HTTPFlow) -> None:
        """
        显示响应的详情字符串

        :return:
        """
        lines = [
            f'\n********** Response {flow.response.status_code} {flow.request.url}  **********',
            f'headers: {format_dict(self.parse_response_headers(flow))}',
            f'cookie: {format_dict(self.parse_response_cookie(flow))}',
            f'content_length: {len(flow.response.content)}'
        ]
        self.logger.debug('\n'.join(lines))

    @staticmethod
    def domain(flow: http.HTTPFlow) -> str:
        """
        获取域名

        :param flow:
        :return:
        """
        return urlparse(flow.request.url).netloc

    def load_file(self, filepath: str, byte: bool = False) -> Union[str, bytes]:
        """
        加载 js 文件

        :return:
        """

        if byte:
            with open(filepath, 'rb') as f:
                return f.read()
        else:
            with open(filepath, 'r', encoding=self.encoding) as f:
                return f.read()

    @staticmethod
    def is_match(pattern: str, target: str, flags=0) -> bool:
        """
        正则是否匹配

        :param pattern: 正则规则
        :param target: 目标
        :return:
        """
        if flags is None:
            flags = 0

        return bool(re.search(r"%s" % pattern, target, flags))

    def is_html(self, flow: http.HTTPFlow) -> bool:
        """
        判断响应的是不是 html 文件

        :param flow:
        :return:
        """
        is_html = False

        if flow.request.url.endswith('html'):
            return True

        headers = self.parse_response_headers(flow)
        if 'Content-Type' in headers and 'text/html' in headers['Content-Type']:
            is_html = True
        elif 'content-type' in headers and 'text/html' in headers['content-type']:
            is_html = True

        return is_html

    def is_js(self, flow: http.HTTPFlow) -> bool:
        """
        判断是否是 js 文件

        :param flow:
        :return:
        """
        is_js = False

        if flow.request.url.endswith(".js"):
            return True

        headers = self.parse_response_headers(flow)
        if 'Content-Type' in headers and 'application/javascript' in headers['Content-Type']:
            is_js = True
        elif 'content-type' in headers and 'application/javascript' in headers['content-type']:
            is_js = True

        return is_js

    def get_encoding(self, flow: http.HTTPFlow) -> str:
        """
        获取响应的编码格式

        :param flow:
        :return:
        """
        if flow.response.content:
            encoding = chardet.detect(flow.response.content)["encoding"]
        else:
            encoding = None

        if not encoding:
            encoding = self.encoding

        return encoding


class Show(MitmproxyBase):
    """
        只是用来打印查看
    """

    def request(self, flow: http.HTTPFlow) -> None:
        """
        请求发起之前处理

        :param flow:
        :return:
        """
        self.show_request_detail(flow)

    def response(self, flow: http.HTTPFlow) -> None:
        """
        响应发送之前处理

        :param flow:
        :return:
        """
        self.show_response_detail(flow)
