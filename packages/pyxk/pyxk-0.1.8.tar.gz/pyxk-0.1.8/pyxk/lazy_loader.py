"""
延迟加载实现
"""
from types import ModuleType
from importlib import import_module



class LazyLoader(ModuleType):
    """
    模块 延迟加载
    :params: local_name: 模块引用名称
    :params: parent_module_globals: 加载全局变量变量
    :params: import_name: 导入模块名称
    """

    def __init__(
        self, local_name, parent_module_globals, import_name,
    ):
        self._local_name = local_name
        self._parent_module_globals = parent_module_globals
        super().__init__(import_name)

    def _loader(self):
        module = import_module(self.__name__)
        self._parent_module_globals[self._local_name] = module
        self.__dict__.update(module.__dict__)
        return module

    def __getattr__(self, name):
        # print(f"LazyLoader.__getattr__: {name!r}")
        module = self._loader()
        return getattr(module, name)

    def __dir__(self):
        module = self._loader()
        return dir(module)
