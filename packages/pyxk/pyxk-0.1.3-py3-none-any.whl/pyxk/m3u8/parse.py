from pyxk.lazy_loader import LazyLoader

os = LazyLoader("os", locals(), "os")
asyncio = LazyLoader("asyncio", locals(), "asyncio")
warnings = LazyLoader("warnings", locals(), "warnings")
hashlib = LazyLoader("hashlib", locals(), "hashlib")
itertools = LazyLoader("itertools", locals(), "itertools")

m3u8 = LazyLoader("m3u8", locals(), "m3u8")
aiohttp = LazyLoader("aiohttp", locals(), "aiohttp")
aiofiles = LazyLoader("aiofiles", locals(), "aiofiles")
panel = LazyLoader("panel", locals(), "rich.panel")
columns = LazyLoader("columns", locals(), "rich.columns")
console = LazyLoader("console", locals(), "rich.console")
progress = LazyLoader("progress", globals(), "rich.progress")

aes = LazyLoader("aes", locals(), "pyxk.aes")
utils = LazyLoader("utils", locals(), "pyxk.utils")
requests = LazyLoader("requests", locals(), "pyxk.requests")



class M3U8ParseInit:
    """
    m3u8解析初始化
    """
    def __init__(self):

        self._m3u8_uri = None
        self._filename = None
        self._filepath = None
        self._m3u8keys = None
        self._duration = None
        self._maximum  = None
        self._limit    = 16
        self._cipher   = {}
        self._serial   = 0

        self._sha1 = lambda x: hashlib.sha1(x).hexdigest()
        self._sava = lambda x, y, z: bool(x and (not os.path.isfile(y) or z))

        self._cs  = console.Console()
        self._req = requests.Session(keep_alive=True)


    @property
    def m3u8_uri(self):
        if not hasattr(self, "_m3u8_uri"):
            setattr(self, "_m3u8_uri", None)
        return getattr(self, "_m3u8_uri")

    @m3u8_uri.setter
    def m3u8_uri(self, value):
        if value is None:
            setattr(self, "_m3u8_uri", None)
            return
        if not isinstance(value, str):
            raise TypeError(
                f"\033[31mm3u8 uri: {str(value)!r} must be a 'str'"
                f", can't be a {type(value).__name__!r}\033[0m")
        if not m3u8.is_url(value):
            raise ValueError(f"\033[31mm3u8 uri:{value!r} must be an absolute link\033[0m")
        setattr(self, "_m3u8_uri", value)

    @property
    def filepath(self):
        if not hasattr(self, "_filepath"):
            setattr(self, "_filepath", os.getcwd())
        return getattr(self, "_filepath") or os.getcwd()

    @filepath.setter
    def filepath(self, value):
        if value is None:
            setattr(self, "_filepath", os.getcwd())
            return
        value = os.path.abspath(value)
        setattr(self, "_filepath", value)

    @property
    def filename(self):
        if not hasattr(self, "_filename"):
            setattr(self, "_filename", None)
        return getattr(self, "_filename")

    @filename.setter
    def filename(self, value):
        if value is None:
            value = "index.mp4"
        elif not isinstance(value, str):
            raise TypeError(
                f"\033[31mfilename:{str(value)!r} must be a 'str'"
                f", can't be a {type(value).__name__!r}\033[0m")
        value = utils.rename(value, self.filepath, "mp4")[0]
        setattr(self, "_filename", value)

    @property
    def limit(self):
        if not hasattr(self, "_limit"):
            setattr(self, "_limit", 16)
        return getattr(self, "_limit")

    @limit.setter
    def limit(self, value):
        if not isinstance(value, int):
            raise TypeError(
                f"\033[31mlimit:{str(value)!r} must be a 'int'"
                f", can't be a {type(value).__name__!r}\033[0m")
        setattr(self, "_limit", value if value > 0 else 16)



class M3U8(M3U8ParseInit):
    """
    m3u8 解析
    """
    def load(
        self,
        uri,
        filename=None,
        filepath=None,
        rereq=False,
        sava=True,
        download=True,
        **kwargs
    ):
        """
        m3u8链接解析
        """
        self.filepath, self.filename, self.m3u8_uri = filepath, filename, uri
        # 获取本地m3u8文件
        m3u8_file = self.__sha1_filename(uri)

        if not rereq and os.path.isfile(m3u8_file):
            with open(m3u8_file) as file:
                content = file.read()
        else:
            kwargs.setdefault("method", "GET")
            content = self._req.request(url=uri, **kwargs).text

        # 使用模块 m3u8 解析
        m3u8obj  = m3u8.loads(content, uri)
        segments = self.__m3u8_paring(m3u8obj, rereq, sava, **kwargs)
        self.__download_merge(segments, download, **kwargs)


    def loads(
        self,
        content,
        uri=None,
        filename=None,
        filepath=None,
        rereq=False,
        sava=True,
        download=True,
        **kwargs
    ):
        """
        m3u8文件解析
        """
        if not isinstance(content, str):
            raise TypeError(
                f"\033[31mcontent must be a 'str'"
                f", can't be a {type(content).__name__!r}\033[0m")

        self.filepath, self.filename, self.m3u8_uri = filepath, filename, uri
        # content 本地文件
        if not content.startswith("#EXTM3U"):
            m3u8file = os.path.abspath(content)
            if os.path.isfile(m3u8file):
                with open(m3u8file) as file:
                    content = file.read()

        m3u8obj  = m3u8.loads(content, uri=uri)
        segments = self.__m3u8_paring(m3u8obj, rereq, sava, **kwargs)
        self.__download_merge(segments, download, **kwargs)


    def probe(self, uri, filename=None, filepath=None, **kwargs):
        """
        测试 m3u8 链接
        """
        self.load(uri, filename, filepath, True, False, False, **kwargs)


    async def __download(self, segments, headers=None):
        """
        异步 下载管理
        """
        default_headers = utils.default_headers()
        default_headers.update(headers or {})

        # m3u8 解密器
        cipher, self._serial = {}, 0
        if self._m3u8keys:
            for index, key in self._m3u8keys.items():
                cipher[index] = aes.Cryptor(**key[1])
        setattr(self, "_cipher", cipher)

        # 进度条
        with progress.Progress(
            *(
                progress.SpinnerColumn("line"),
                progress.TextColumn("[progress.description]{task.description}"),
                progress.BarColumn(),
                progress.TaskProgressColumn(),
                progress.TimeElapsedColumn(),
            ),
            console=self._cs,
        ) as _progress:

            # 为进度条条添加一个任务
            progress_task = _progress.add_task(
                f"[magenta]0/{self._maximum}[/]", total=self._maximum)

            # 开启异步 session
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=2*60),
                connector=aiohttp.TCPConnector(limit=self.limit),
                headers=default_headers
            ) as session:

                # 创建异步任务
                tasks, segment_folder = [], \
                    os.path.join(self.filepath, f".{self.filename.rsplit('.', 1)[0]}", "segments")
                if not os.path.isdir(segment_folder):
                    os.makedirs(segment_folder)

                for index, segment in segments.items():

                    task = self.__arequest(
                        session,
                        file=os.path.join(segment_folder, f"{index}.ts"),
                        _progress=_progress,
                        _task=progress_task,
                        **segment)
                    tasks.append(task)

                await asyncio.gather(*tasks)
        print()


    async def __arequest(self, session, uri, file, _progress, _task, sign=None):
        """
        异步 下载
        """
        if os.path.isfile(file):
            # 文件存在, 更新进度条
            self._serial += 1
            _progress.update(
                _task, advance=1,
                description=f"[magenta]{self._serial}/{self._maximum}[/]",)
            return

        while True:
            try:
                async with session.get(uri) as response:
                    # 异常状态码捕获
                    if 403 <= response.status <= 410:
                        raise aiohttp.InvalidURL(
                                f"invalid url:\033[4;31m{str(response.url)!r}\033[0m, "
                                f"status_code: \033[31m{response.status!r}\033[0m")

                    await self.__media_write(
                        file, await response.content.read(), sign)
                    break

            # 请求超时 重试
            except asyncio.exceptions.TimeoutError:
                # warnings.warn(f"Timeout")
                await asyncio.sleep(1)

            # 连接错误 重试
            except (
                aiohttp.client_exceptions.ClientOSError,
                aiohttp.client_exceptions.ClientConnectorError,
            ):
                warnings.warn("\033[33m连接错误, 请检查网络是否正常 !!!\033[0m")
                await asyncio.sleep(1)

        # 下载完成, 更新进度条
        self._serial += 1
        _progress.update(
            _task, advance=1,
            description=f"[magenta]{self._serial}/{self._maximum}[/]",)


    async def __media_write(self, file, content, sign=None):
        """
        保存 视频媒体
        """
        if sign is not None:
            content = self._cipher[sign].decrypt(content)
        async with aiofiles.open(file, "wb") as _file:
            await _file.write(content)


    def __download_merge(self, segments, download, **kwargs):
        """
        异步下载 并 合并
        """
        if download and segments:
            asyncio.run( self.__download(segments, kwargs.get("headers", {})) )


    def __m3u8_paring(self, m3u8obj, rereq=False, sava=True, **kwargs):
        """
        m3u8 解析方法
        """
        m3u8obj = self.__playlists_paring(m3u8obj, rereq, sava, **kwargs)
        self.__m3u8keys_paring(m3u8obj, rereq, sava, **kwargs)
        segments = self.__segments_paring(m3u8obj, rereq, sava)

        # 可视化解析结果
        _display = [
            f"URI: {self.m3u8_uri}",
            f"FileName: [magenta]{self.filename}[/]",
            f"FilePath: {self.filepath}",
            f"PlayTime: {utils.human_playtime_pr(self._duration)}",
            f"Maximum: {self._maximum}",
            f"M3U8Keys: {bool(self._m3u8keys)}",
            f"Limit: {self.limit}"
        ]
        _display = [f"{i+1} {x}" for i, x in enumerate(_display)]
        if segments:
            _display.append("[green b]Parsing success !!![/]")
        else:
            _display.append("[red b]Parsing failure: segments not found !!![/]")

        _columns = columns.Columns(_display)
        _panel   = panel.Panel(_columns, title="M3U8 Parsed", border_style="yellow")
        self._cs.print(_panel)
        return segments


    def __playlists_paring(self, m3u8obj, rereq=False, sava=True, **kwargs):
        """
        解析 playlists
        播放列表包含多个m3u8链接 选择带宽最大的下载
        """
        # 没有playlists
        if not m3u8obj.is_variant:
            return m3u8obj

        # 根据 playlists 带宽正序排序
        playlists = sorted(
            [
                (item.absolute_uri, item.stream_info.bandwidth)
                for item in m3u8obj.playlists
            ],
            key=lambda x: x[1])

        playlists_file = self.__sha1_filename(
            self.m3u8_uri or self.filename+"playlists")

        # 保存playlists 至本地文件
        if self._sava(sava, playlists_file, rereq):
            for playlist in m3u8obj.playlists:
                playlist.uri = playlist.absolute_uri
            m3u8obj.dump(playlists_file)

        self.m3u8_uri = uri = playlists[-1][0]
        playlists_file = self.__sha1_filename(uri)

        # 获取本地文件 playlists
        if not rereq and os.path.isfile(playlists_file):
            with open(playlists_file) as file:
                content = file.read()
        else:
            content = self._send(uri, **kwargs).text

        m3u8obj = m3u8.loads(content, uri)
        return self.__playlists_paring(m3u8obj, rereq, sava, **kwargs)


    def __m3u8keys_paring(self, m3u8obj, rereq=False, sava=True, **kwargs):
        """
        解析 keys
        破解m3u8加密
        """
        m3u8keys = dict(enumerate([key for key in m3u8obj.keys if key]))

        for index, key in m3u8keys.copy().items():
            keyuri = key.uri = key.absolute_uri
            keyfile = self.__sha1_filename(keyuri, suffix=".key")

            # 从本地文件密钥
            if not rereq and os.path.isfile(keyfile):
                with open(keyfile, "rb") as file:
                    secret = file.read()
            else:
                secret = self._send(keyuri, **kwargs).content

            # 保存密钥至本地文件
            if self._sava(sava, keyfile, rereq):
                with utils.make_open(keyfile, "wb") as file:
                    file.write(secret)
            # 获取 iv
            m3u8iv = key.iv.removeprefix("0x")[:16].encode() \
                if key.iv else secret[:16]
            m3u8keys[index] = (keyuri, {"key": secret, "iv" : m3u8iv})
        # 保存 m3u8 keys
        setattr(self, "_m3u8keys", m3u8keys or None)


    def __segments_paring(self, m3u8obj, rereq=False, sava=True):
        """
        解析 segments
        获取所有的segments片段 进行异步下载
        """
        # 没有segments数据 链接可能不是m3u8
        if not m3u8obj.is_endlist:
            self._duration, self._maximum = None, None
            return {}

        segments_file = self.__sha1_filename(
            self.m3u8_uri or self.filename+"segments")

        # 解析segments
        segments, duration = {}, 0
        for index, segment in enumerate(m3u8obj.segments):
            segment.uri, sign = segment.absolute_uri, None
            duration += segment.duration
            # 对比 keyuri
            if segment.key:
                s_keyurl = segment.key.absolute_uri
                for i, key in self._m3u8keys.items():
                    if s_keyurl == key[0]:
                        sign = i
                        break
            # 保存所有segments
            segments[index] = {"uri": segment.uri, "sign": sign}

        # 保存 segments 至本地文件
        if self._sava(sava, segments_file, rereq):
            m3u8obj.dump(segments_file)

        setattr(self, "_duration", duration)
        setattr(self, "_maximum", len(segments))
        return segments


    def _send(self, uri, **kwargs):

        kwargs.setdefault("method", "GET")
        if self.m3u8_uri:
            kwargs.setdefault("headers", {})
            headers = kwargs["headers"]
            headers["Referer"] = self.m3u8_uri

        return self._req.request(url=uri, **kwargs)


    def __sha1_filename(self, uri, suffix=".m3u8"):

        filename = self.filename.rsplit('.', 1)[0]
        return os.path.join(
            self.filepath, f".{filename}",
            self._sha1(uri.encode()) + suffix)
