
def float_lists_equal(list1, list2, epsilon=1e-6):
    res = (abs(a - b) < epsilon for a, b in zip(list1, list2))
    return all(res)