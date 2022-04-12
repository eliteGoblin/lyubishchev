# pls refer to https://stackoverflow.com/questions/44834/can-someone-explain-all-in-python
# takeaway:
#  __all__ used for "friendly reminder", can't stop some name be exposed, can still be seen using dir(name)
#  __all__ take effect in various level of module's __init__ files.
from .sub_1 import *
from .sub_2 import *

__all__ = ["sub1_func"]  # restrict "exported" name in different level
