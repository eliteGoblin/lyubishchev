from typing import Any


def prune_dict(input_dict: dict[str, Any]) -> None:
    """
    Remove empty dicts and 0 values from dict
    {
        "key1": {
            "key11": 11,
            "key12": 0,
        },
        "key2": {}
    }
    will get
    {
        "key1": {
            "key11": 11,
        }
    }
    """
    if input_dict is None:
        return

    keys_to_remove = []

    for key, value in input_dict.items():
        if isinstance(value, dict):
            prune_dict(value)
        if not value:
            keys_to_remove.append(key)
        elif value == 0:
            keys_to_remove.append(key)

    for key in keys_to_remove:
        del input_dict[key]


def sum_dict_values(dct: dict[str, Any]) -> int:
    """
    sum all values in a dict, if value is a dict, sum it recursively
    """
    if isinstance(dct, dict):
        return sum(sum_dict_values(v) for v in dct.values())
    return dct
