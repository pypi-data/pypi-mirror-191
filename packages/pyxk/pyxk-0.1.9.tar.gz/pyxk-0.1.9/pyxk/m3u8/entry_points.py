import json
import argparse
from pyxk.m3u8 import M3U8



def use_argparse():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "uri", help="需要下载的m3u8链接")
    parser.add_argument(
        "-fn", "--filename", help="媒体文件名称")
    parser.add_argument(
        "-fp", "--filepath", help="媒体文件路径")
    parser.add_argument(
        "-r", "--rereq", help="重新下载(default: False)", action="store_true")
    parser.add_argument(
        "-s", "--sava", help="保存m3u8文本文件(default: True)", action="store_false")
    parser.add_argument(
        "-d", "--download", help="下载ts文件(default: True)", action="store_false")
    parser.add_argument(
        "-rm", "--remove", help="合并完成删除ts文件(default: True)", action="store_false")
    parser.add_argument(
        "-l", "--limit", help="异步aiohttp并发连接(default: 16)", default=16, type=int)
    parser.add_argument(
        "-p", "--probe", help="测试m3u8链接(default: False)", action="store_true")
    parser.add_argument(
        "--parameter", help="Request 参数(type: dict)", default='{}', type=json.loads)
    return parser.parse_args()



def main():

    args = use_argparse()
    m3u8obj = M3U8()
    m3u8obj.limit = args.limit

    if args.probe is True:
        m3u8obj.probe(
            uri=args.uri,
            filename=args.filename,
            filepath=args.filepath,
            **args.parameter)
        return

    m3u8obj.load(
        uri=args.uri,
        filename=args.filename,
        filepath=args.filepath,
        rereq=args.rereq,
        sava=args.sava,
        download=args.download,
        remove=args.remove,
        **args.parameter)
