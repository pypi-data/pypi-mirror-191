"""
AES 加解密
"""
from pyxk.lazy_loader import LazyLoader

copy = LazyLoader("copy", globals(), "copy")
AES = LazyLoader("AES", globals(), "Crypto.Cipher.AES")
fmtdata = LazyLoader("fmtdata", globals(), "pyxk.aes._fmtdata")



def no_padding(data, remove=False, pad=b"\x00"):
    """
    NoPadding填充模式
    """
    # 消除 padding 字符
    if remove:
        return data.rstrip(pad)
    remainder = len(data) % AES.block_size or AES.block_size
    data += pad * (AES.block_size - remainder)
    return data


def zero_padding(data, remove=False, pad=b"\x00"):
    """
    ZeroPadding填充模式
    """
    # 消除 padding 字符
    if remove:
        return data.rstrip(pad)
    remainder = len(data) % AES.block_size
    # 不填充
    data += pad * (AES.block_size - remainder)
    return data


PADDING_ALL = {
    "Raw": lambda data, *args, **kwagrs: data,
    "NoPadding": no_padding,
    "ZeroPadding": zero_padding,
}



class Cryptor(fmtdata.FormatData):
    """
    AES加解密
    """

    def __init__(
        self, key, iv=None, mode="CBC", padding="NoPadding", **kwargs
    ):
        self._cipher = None
        self._padding = padding
        self.__padding_fmt()
        super().__init__(key, iv, mode, **kwargs)


    def __padding_fmt(self):
        """
        加解密数据的填充方式
        """
        padding = getattr(self, "_padding", None)
        if padding is None:
            setattr(self, "_padding", "NoPadding")
            return

        if (
            not isinstance(padding, str)
            or padding not in PADDING_ALL
        ):
            raise ValueError(
                f"\033[31m'padding' must exist in the {list(PADDING_ALL)},"
                f" not '{padding}'\033[0m")


    def encrypt(self, plaintext):
        """
        加密
        """
        if isinstance(plaintext, str):
            plaintext = plaintext.encode(self._encode)

        elif not isinstance(plaintext, bytes):
            raise TypeError(
                "\033[31m'plaintext' type must be 'str' or 'bytes',"
                f" not '{type(plaintext).__name__}'\033[0m")

        # 创建 cipher - 加密
        self.__create_cipher()
        padding_func = PADDING_ALL[self.padding]
        return self._cipher.encrypt( padding_func(plaintext) )


    def decrypt(self, ciphertext):
        """
        解密
        """
        if isinstance(ciphertext, str):
            ciphertext = ciphertext.encode(self._encode)

        elif not isinstance(ciphertext, bytes):
            raise TypeError(
                "\033[31m'plaintext' type must be 'str' or 'bytes',"
                f" not '{type(ciphertext).__name__}'\033[0m")

        # 创建 cipher - 解密
        self.__create_cipher()
        padding_func = PADDING_ALL[self.padding]
        return padding_func(self._cipher.decrypt(ciphertext), True)


    def __create_cipher(self):
        """
        创建 cipher
        """
        state = copy.deepcopy(self._state)
        state["key"]  = self.key
        state["mode"] = self.mode
        if self.iv is not None:
            state["iv"] = self._iv
        setattr(self, "_cipher", AES.new(**state))


    @property
    def padding(self):
        if not hasattr(self, "_padding"):
            setattr(self, "_padding", "NoPadding")
        return getattr(self, "_padding")


    @padding.setter
    def padding(self, value):
        setattr(self, "_padding", value)
        self.__padding_fmt()



if __name__ == "__main__":

    from pprint import pprint

    raw_text = b"Hello World"
    key = b"1234567890123456"

    # cipher
    cipher = AESCryptor(key)
    cipher.padding = "ZeroPadding"
    cipher.iv  = key[::-1]

    ciphertext = cipher.encrypt(raw_text)
    plaintext  = cipher.decrypt(ciphertext)

    print(raw_text)
    print(ciphertext)
    print(plaintext)

    pprint(cipher.__dict__)
