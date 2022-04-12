from package_inner.inner import inner_func


def outter_func() -> bool:
    return inner_func()
