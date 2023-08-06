# coding=utf-8

import re
import unicodedata


def nfkd_normalized(text) -> str:
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')

def nfkd_normalized_lower(text) -> str:
    return nfkd_normalized(text).lower()

def nfkd_normalized_lower_no_spec(text) -> str:
    nfkd_normalized = nfkd_normalized_lower(text)
    return re.sub('[^a-z0-9]+', '', nfkd_normalized)

def nfkd_normalized_lower_db_safe(text) -> str:
    nfkd_normalized = nfkd_normalized_lower(text)
    return re.sub('[^a-z0-9_]+', '', nfkd_normalized)

def camel_case_to_snake_case(key: str):
    """ Convert camel case string to snake case. For example: SomeName to some_name """
    return re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()


def empty_str_to_none(value: str):
    if isinstance(value, str) and len(value.strip()) == 0:
        return None
    return value


def year_zero_to_none(value: str):
    if value == '0000-00-00 00:00:00':
        return None
    return value

def get_dict_item_might_not_exists(names: dict, key):
    if names is None:
        return key
    try:
        return names[key]
    except KeyError:
        return key
