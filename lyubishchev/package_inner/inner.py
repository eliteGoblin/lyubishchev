from package_inner.sub_1.sub1 import sub1_func
from package_inner.sub_2.sub2 import sub2_func


def inner_func() -> bool:

    return sub1_func() and sub2_func() and True
