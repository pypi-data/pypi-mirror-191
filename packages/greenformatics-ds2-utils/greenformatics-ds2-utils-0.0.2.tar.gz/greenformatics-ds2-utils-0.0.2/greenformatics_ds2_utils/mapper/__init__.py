# coding=utf-8

from  greenformatics_ds2_utils.converter import *
import json

def dict_to_object_in_snake_case(data, obj, names=None):
    """ Map dict with camel case keys to an object with snake case attributes """
    o = obj()
    for k, v in data.items():
        if isinstance(v, list) or isinstance(v, dict):
            setattr(o, nfkd_normalized_lower(camel_case_to_snake_case(get_dict_item_might_not_exists(names, k))),
                    json.dumps(v))
        else:
            setattr(o, nfkd_normalized_lower(camel_case_to_snake_case(get_dict_item_might_not_exists(names, k))),
                year_zero_to_none(empty_str_to_none(v)))
    return o

def dict_to_object_in_lower_case_no_spec(data, obj, names=None):
    """ Map dict with camel case keys to an object with snake case attributes """
    o = obj()
    for k, v in data.items():
        if isinstance(v, list) or isinstance(v, dict):
            setattr(o, nfkd_normalized_lower_no_spec(get_dict_item_might_not_exists(names, k)), json.dumps(v))
        else:
            setattr(o, nfkd_normalized_lower_no_spec(get_dict_item_might_not_exists(names, k)),
                    year_zero_to_none(empty_str_to_none(v)))
    return o

def dict_to_object_in_lower_case_db_safe(data, obj, names=None):
    """ Map dict with camel case keys to an object with snake case attributes """
    o = obj()
    for k, v in data.items():
        if isinstance(v, list) or isinstance(v, dict):
            setattr(o, nfkd_normalized_lower_db_safe(get_dict_item_might_not_exists(names, k)), json.dumps(v))
        else:
            setattr(o, nfkd_normalized_lower_db_safe(get_dict_item_might_not_exists(names, k)),
                    year_zero_to_none(empty_str_to_none(v)))
    return o

def dict_list_to_object_list(dict_list: [{}], obj, names=None) -> []:
    """ Loop through the list of dictionaries and map them to objects. It results a list of object. """
    object_list = []
    for elem in dict_list:
        object_list.append(dict_to_object_in_snake_case(elem, obj, names))
    return object_list
