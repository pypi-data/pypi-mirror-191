"""
import pyxk.utils
"""
from pyxk.lazy_loader import LazyLoader
re = LazyLoader("re", globals(), "re")
os = LazyLoader("os", globals(), "os")
base64 = LazyLoader("base64", globals(), "base64")
hashlib = LazyLoader("hashlib", globals(), "hashlib")
difflib = LazyLoader("difflib", globals(), "difflib")
multidict = LazyLoader("multidict", globals(), "multidict")
functools = LazyLoader("functools", globals(), "functools")
itertools = LazyLoader("itertools", locals(), "itertools")
collections = LazyLoader("collections", globals(), "collections")



def open_decorator(built_in_open):
    """
    内置函数 open 装饰器
    作用: 写或追加模式下 创建不存在的目录
    """
    @functools.wraps(built_in_open)
    def wrapper(file, mode="r", **kwargs):
        # 判断 mode 是否属于写或追加模
        # collections.Counter 统计可迭代对象 每项出现的次
        # itertools.product 求多个可迭代对象的笛卡尔积
        create_mode = [collections.Counter(i+j) for i in ("w", "a") for j in ("b", "+", "b+", "")]
        # 创建目录
        if isinstance(mode, str) and collections.Counter(mode) in create_mode:
            folder = os.path.dirname(file)
            if not os.path.isdir(folder):
                os.makedirs(folder)
        return built_in_open(file, mode, **kwargs)
    return wrapper
make_open = open_decorator(open)


def is_base64(data: str or bytes) -> bool:
    """
    判断base64数据类型 return: bool
    """
    if isinstance(data, bytes):
        # base64 数据类型 正则表达式判断
        B64_RE_PATTERN_B = re.compile(rb"^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$")
        return bool(B64_RE_PATTERN_B.match(data))

    if isinstance(data, str):
        # base64 数据类型 正则表达式判断
        B64_RE_PATTERN   = re.compile(r"^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$")
        return bool(B64_RE_PATTERN.match(data))
    # str 或 bytes 以外类型返回 False
    return False


def tobytes_from_base64(data: str or bytes, encoding="UTF-8"):
    """
    base64数据类型 转化为bytes
    如果不为base64数据类型 则返回原始数据
    """
    if (
        not isinstance(data, (str, bytes))
        or not is_base64(data)
    ):
        return False, data
    if isinstance(data, str):
        data = data.encode(encoding)
    return True, base64.b64decode(data)


# User-Agnet
UA_ANDROID  = "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36"
UA_WINDOWNS = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
UA_MAC      = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
UA_IPHONE   = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
UA_IPAD     = "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1"
UA_SYMBIAN  = "Mozilla/5.0 (Symbian/3; Series60/5.2 NokiaN8-00/012.002; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/533.4 (KHTML, like Gecko) NokiaBrowser/7.3.0 Mobile Safari/533.4 3gpp-gba"
UA_APAD     = "Mozilla/5.0 (Linux; Android 11; Phh-Treble vanilla Build/RQ3A.211001.001;) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.91 Safari/537.36"

UA_ALL = {
    "android" : UA_ANDROID,
    "windows" : UA_WINDOWNS,
    "mac"     : UA_MAC,
    "iphone"  : UA_IPHONE,
    "ipad"    : UA_IPAD,
    "symbian" : UA_SYMBIAN,
    "apad"    : UA_APAD
}


def get_user_agent(user_agent, overwrite=False):
    """
    获取 UserAgent
    """
    if not isinstance(user_agent, str):
        raise ValueError(
            f"\033[31minvalid user_agent: '{user_agent}', "
            f"type: '{type(user_agent).__name__}'\033[0m")
    # 重写
    if overwrite is True:
        return user_agent

    user_agent = difflib.get_close_matches(user_agent.lower(), UA_ALL, 1)
    if not user_agent:
        return UA_ANDROID
    return UA_ALL[user_agent[0]]


def default_headers():
    """
    默认 Headers
    """
    headers = (("User-Agent", get_user_agent("android")),)
    return multidict.CIMultiDict(headers)


def md5(data: str or bytes, encoding="UTF-8"):
    """
    md5加密
    """
    if isinstance(data, str):
        data = data.encode(encoding=encoding)

    elif not isinstance(data, bytes):
        raise TypeError(
            "\033[31mmd5 encrypted data must be a 'str' or 'bytes'"
            f", can't be a {type(data).__name__!r}\033[0m")
    return hashlib.md5(data).hexdigest()


def rename(filename, filepath, suffix=""):
    """
    重命名本地存在的文件
    """
    if suffix:
        suffix = "." + suffix.removeprefix(".")
    else:
        suffix = ""
    if not filename.endswith(suffix):
        filename += suffix
    # 完整文件路径
    file = os.path.join(filepath, filename)

    # 重命名
    for i in itertools.count(1):
        if not os.path.isfile(file):
            if i != 1:
                filename = os.path.basename(file)
            break

        file = os.path.join(
            filepath,
            filename.removesuffix(suffix) + f".{i}{suffix}")
    return filename, file


def human_playtime_pr(playtime):
    """
    人类直观时间展示
    """
    if not isinstance(playtime, (int, float)):
        if playtime is None:
            return None
        raise TypeError(
            f"\033[31mhuman_playtime_pr parameter 'playtime' must be a 'int' or 'float'"
            f", can't be a {type(playtime).__name__!r}\033[0m")
    hour, second   = divmod(round(playtime), 3600)
    minute, second = divmod(second, 60)
    return f"{hour}:{minute:0>2}:{second:0>2}"


def hash256(data, encoding="UTF-8"):
    """
    hash256
    """
    if isinstance(data, str):
        data = data.encode(encoding)
    return hashlib.sha256(data).hexdigest()


