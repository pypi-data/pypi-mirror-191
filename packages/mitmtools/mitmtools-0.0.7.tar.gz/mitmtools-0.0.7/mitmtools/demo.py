"""
    这只是一个配置的例子
    
    注意：
        启动之后，文件是动态的，随时修改随时生效
        启动程序要和该程序在同一目录，不然可能找不到文件路径
        使用中要注意缓存的影响，停用缓存或清除缓存再尝试
"""
from mitmtools import Show
from mitmtools.remove import RemoveContent
from mitmtools.hook import HookJs, HookHtml
from mitmtools.replace import ReplaceByStr, ReplaceByFile

addons = [
    Show(),  # 输出请求、响应

    # replace
    # ReplaceByStr(pattern='https://www.baidu.com/', replace_dict={'百度一下，你就知道': '百度一下，你也不知道'})
    # ReplaceByFile(pattern='^https://www.baidu.com.?$', filepath="./mitmtools/static/index.html")

    # hook
    # HookHtml(pattern='https://www.baidu.com/', filepath='./mitmtools/static/hookCookie.js'),
    # HookHtml(pattern='https://www.baidu.com/', content='''
    #     (function () {
    #         var gkDocument = document;
    #         var gkPrint = console.log;
    #         Object.defineProperty(document, "cookie", {
    #             set: function (val) {
    #                 gkPrint("正在设置 Cookie：", val)
    #                 debugger;
    #                 cookieTemp = val;
    #                 return val
    #             },
    #             get: function () {
    #                 return gkDocument.cookie
    #             }
    #         })
    #     })()
    # '''),
    HookJs(
        pattern="san_b247717.js",
        filepath='./mitmtools/static/hookCookie.js'
    ),

    # remove
    # RemoveContent(pattern='https://www.baidu.com/', remove_list=['就知道'])
]
