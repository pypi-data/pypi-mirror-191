# coding=utf-8

import re
import unicodedata


def nfkd_normalized(text) -> str:
    """ Remove accents of all the national characters. For example hungarian \"á\" and german \"ä\" both are converted
    to \"a\".

    :param text: the string to be converted

    :returns: A UTF-8 encoded string without accents.  If the input was None, it remains None.
    """

    if text is None:
        return None

    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')


def nfkd_normalized_lower(text) -> str:
    """ Remove accents of all the national characters and transform the result to lower case string. For example
    hungarian \"Á\" and german \"Ä\" both are converted to \"a\".

    :param text: the string to be converted

    :returns: A UTF-8 encoded string without accents in lower case format.  If the input was None, it remains None.
    """

    if text is None:
        return None

    return nfkd_normalized(text).lower()


def nfkd_normalized_lower_no_spec(text) -> str:
    """ Remove accents of all the national characters and all the special characters and transform the result
    to lower case string. For example hungarian \"Á B C\" and german \"Ä Bc\" both are converted to \"abc\".

    :param text: the string to be converted

    :returns: A UTF-8 encoded string without accents and special characters in lower case format. If the input was None,
    it remains None.
    """

    if text is None:
        return None

    normalized_text = nfkd_normalized_lower(text)
    return re.sub('[^a-z0-9]+', '', normalized_text)


def nfkd_normalized_lower_db_safe(text) -> str:
    """ Remove accents of all the national characters and all the special characters except \"_\" (underscore)
    and transform the result to lower case string. For example hungarian \"Á B_[C]\" and german \"Ä B_[c]\"
    both are converted to \"ab_c\".

    :param text: the string to be converted

    :returns: A UTF-8 encoded string without accents and special characters except \"_\" (underscore) in lower case
    format.  If the input was None, it remains None.
    """

    if text is None:
        return None

    normalized_text = nfkd_normalized_lower(text)
    return re.sub('[^a-z0-9_]+', '', normalized_text)


def camel_case_to_snake_case(key) -> str:
    """ Convert camel case string to snake case. Also remove accents of all the national characters. For example:
    SomeName to some_name.

    :param key: the string to be converted

    :returns: It returns a UTF-8 encoded string without accents and special characters except \"_\" (underscore)
    in snake case format.  If the input was None, it remains None
    """

    if key is None:
        return None

    normalized_key = nfkd_normalized(key)
    snake_case_key = re.sub(r'(?<!^)(?=[A-Z])', '_', normalized_key)
    # Remove multiple underscores
    return re.sub(r'_+', '_', snake_case_key).lower()


def empty_str_to_none(value):
    """ Convert an empty string to None. It is useful when you want to persist null value in a database
    instead of an empty string.

    :param value: the value to be tested and to be converted to None if empty
    :return: ``None``, if the value was an empty string or None otherwise the value itself
    """

    if isinstance(value, str) and len(value.strip()) == 0:
        return None
    return value


def year_zero_to_none(value):
    """ Convert a zero date (\"0000-00-00\") to None. It is useful when you want to persist null value
    in a database instead of such a date.

    :param value: the value to be tested and converted to None
    :return: ``None``, if the value was a zero date string or None otherwise the value itself
    """

    if value in ['0000-00-00 00:00:00', '0000-00-00']:
        return None
    return value


def map_attribute_name(attribute_name_map, attribute_name):
    """ Check the key in names. Useful in attribute name mapping: if the attribute name mapping (``attribute_name_map``)
    contains the ``attribute_name``, it returns the mapped attribute name otherwise the original attribute name.

    It is mostly used by the mapper module.

    :param attribute_name_map: the dictionary contains the attribute name map
    :param attribute_name: the attribute name to be mapped or kept if id does not exist in the map
    :return: the mapped attribute name
    """

    if attribute_name_map is None:
        return attribute_name

    try:
        return attribute_name_map[attribute_name]
    except KeyError:
        return attribute_name
