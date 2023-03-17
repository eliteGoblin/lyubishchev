def float_lists_equal(
    list1: list[float], list2: list[float], epsilon: float = 1e-6
) -> bool:
    return all(abs(a - b) < epsilon for a, b in zip(list1, list2))
