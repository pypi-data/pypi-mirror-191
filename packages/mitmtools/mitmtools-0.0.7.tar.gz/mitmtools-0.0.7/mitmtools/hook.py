"""
    进行 js hook
    提供如下三种方法
        HookHtml     通过正则匹配 url，通过 html 进行插入 script 标签进行注入
        HookJs       通过正则匹配 url，通过 js 进行注入

    注意：针对 html
        Content-Security-Policy 简称 csp 可以防止 xss 注入，一般在请求头或者 meta 标签里会有受信任的白名单
        学习链接：http://www.ruanyifeng.com/blog/2016/09/csp.html
        学习链接：https://blog.csdn.net/qq_25623257/article/details/90473859
        因此注入的代码将不会被执行

        突破 csp 的方法（有验证的话也没有用，网页不会正常加载）
            1、手动添加 b"script-src 'self' " 并保证请求头无 nonce-hash 的值
            2、将 nonce-hash 的值放在 script 标签上，none='hash'

    注意：所有方法都可能会被检测影响页面运行，但是方法能出来
"""
from loguru import logger
from mitmproxy import http
from bs4 import BeautifulSoup
from mitmtools.base import MitmproxyBase


class HookBase(MitmproxyBase):
    def __init__(self, pattern: str, filepath: str = None, content: str = None, **kwargs):
        """

        :param pattern: 正则匹配 url
        :param filepath: 注入的文件
        :param content: 注入的内容
        """
        super().__init__(**kwargs)
        self.pattern = pattern
        self.filepath = filepath
        self.content = content
        self.kwargs = kwargs
        self.kwargs.setdefault("flags", 0)  # 正则的 flags


class HookHtml(HookBase):
    """
        hook html 页面
    """

    def __init__(self, pattern: str, filepath: str = None, content: str = None, **kwargs):
        super().__init__(pattern=pattern, filepath=filepath, content=content, **kwargs)

    def response(self, flow: http.HTTPFlow) -> None:
        """
        如果响应是 html 则注入 hook
        增加一个 html script 标签

        注意：如果有检测 script 长度的可能会无效
        :param flow:
        :return:
        """
        if not self.is_match(pattern=self.pattern, target=flow.request.url, flags=self.kwargs["flags"]):
            return

        # 构造节点并插入 hook
        if self.is_html(flow) and flow.response.content:
            # 构造节点
            soup_text = BeautifulSoup(flow.response.text, 'lxml')
            tag = soup_text.new_tag(name='script')

            # 加载脚本
            if self.filepath:
                tag.string = self.load_file(self.filepath)
            elif self.content:
                tag.string = self.content

            # 插入节点
            head = soup_text.find('head')
            if head:
                head.insert(0, tag)
            else:
                soup_text.find('body').insert(0, tag)

            # 替换响应
            flow.response.text = soup_text.__str__()

            # 是否有 csp 有就警告
            self.has_csp(flow)

            logger.debug(f'已注入 js：{flow.request.url}')

    def has_csp(self, flow: http.HTTPFlow) -> bool:
        """
        判断有无 csp 安全策略

        :return:
        """
        resp = flow.response
        if resp:
            headers = self.parse_response_headers(flow)
            if headers.get('content-security-policy') or headers.get('Content-Security-Policy'):
                logger.warning("网站已启用 CSP 防护，注入将不会生效！")
                return True
            elif 'content-security-policy' in resp.text or 'Content-Security-Policy' in resp.text:
                logger.warning("网站已启用 CSP 防护，注入将不会生效！")
                return True

        return False


class HookJs(HookBase):
    """
        hook js 文件
    """

    def __init__(self, pattern: str, filepath: str = None, content: str = None, **kwargs):
        super().__init__(pattern=pattern, filepath=filepath, content=content, **kwargs)

    def response(self, flow: http.HTTPFlow) -> None:
        """
        如果响应是 js 直接注入代码

        :param flow:
        :return:
        """
        if not self.is_match(pattern=self.pattern, target=flow.request.url, flags=self.kwargs["flags"]):
            return

        if self.is_js(flow) and flow.response.content:
            encoding = self.get_encoding(flow)
            flow.response.content = (self.load_file(self.filepath) + '\n').encode(encoding) + flow.response.content
            logger.debug(f'已注入 js：{flow.request.url}')
