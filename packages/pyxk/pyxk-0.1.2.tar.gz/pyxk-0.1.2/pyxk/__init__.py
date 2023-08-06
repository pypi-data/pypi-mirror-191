"""
pip install -U pyxk -i https://pypi.org/simple
"""
import os
import importlib



__all__ = [
   item.removesuffix(".py")
   for item in os.listdir(os.path.dirname(__file__))
   if item not in ("__pycache__", "__init__.py")
]

def __getattr__(name):
   # print(f"{__name__!r}.__getattr__: {name!r}")
   if name not in __all__:
       raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
   return importlib.import_module(f".{name}", package=__name__)

def __dir__():
   return __all__
