import re


def dicts_into_list(dict_of_dicts: dict) -> list[dict]:
    """
    Converts dict of dicts into list structure.
    :param dict_of_dicts: Dict of dicts
    """
    return [item for _, item in dict_of_dicts.items()]


def sort_list_of_dicts(list_of_dicts: list[dict], sort_by: str) -> list[dict]:
    """
    Sort list of dicts by selected column.
    :param list_of_dicts: Input dict
    :param sort_by: Column name. To change direction of sort add +/- at the end of column name. Example: "id-"
    """
    sort_direction = "+"
    sort_order_match = re.match(r".*[+-]$", sort_by)
    if sort_order_match:
        sort_direction = sort_by[-1]
        sort_by = sort_by[:-1]
    result_list = sorted(list_of_dicts, key=lambda item_: item_[sort_by], reverse=(sort_direction == "-"))
    return result_list


def dict_pass(d: dict, attributes: list) -> dict:
    """
    Whitelist dictionary attributes.
    :param d: Dict instance
    :param attributes: Whitelisted attributes
    :return: New instance of filtered dict
    """
    return {key: value for key, value in d.items() if key in attributes}


def dict_filter(d: dict, attributes: list) -> dict:
    """
    Blacklist dictionary attributes.
    :param d: Dict instance
    :param attributes: Blacklisted attributes.
    :return: New instance of filtered dict
    """
    return {key: value for key, value in d.items() if key not in attributes}


def dict_swap(d: dict) -> dict:
    """
    Swap dict keys into values and values into keys.
    :param d: Dict to be swapped
    """
    return {str(value): key for key, value in d.items()}


def list_into_dict(l: list) -> dict:
    """
    Converts list into dict where dict keys are list indexes.
    :param l: List of items
    """
    return dict(enumerate(l))


def map_dict_into_list(d: dict, keys_map: list):
    """
    Maps dict keys into list positions based on keys_map defined in key map list.
    Example:
        d = {"a": "A value", "b": "B value", "c": "C value", "d": "D value"}
        map = ["c", "a", "b", "d"]
        ===>
        ["C value", "A value", "B value", "D value"]
    :param d: Dict to be mapped
    :param keys_map: List of keys order
    """
    result = [None] * len(keys_map)
    map_of_keys = dict_swap(list_into_dict(keys_map))

    for key, value in d.items():
        list_index = map_of_keys[key]
        result[list_index] = value
    return result
