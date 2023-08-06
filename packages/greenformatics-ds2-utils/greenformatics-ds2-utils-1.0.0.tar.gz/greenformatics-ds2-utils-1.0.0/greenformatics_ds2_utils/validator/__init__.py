# coding=utf-8

import requests
import json
import os
from datetime import datetime, date
from greenformatics_ds2_utils.validator.slugvalidator import SlugValidator


def is_url_valid(url: str, base_auth_user=None, base_auth_pass=None) -> int:
    try:
        if base_auth_user:
            session = requests.Session()
            session.auth = (base_auth_user, base_auth_pass)
            request = session.get(url)
        else:
            request = requests.get(url)
        return request.status_code
    except:
        return 404


def is_slug_valid(slug: str, slug_length=255, slug_postfix=None) -> str:
    i = 2
    slg = slug
    sv = SlugValidator()
    while sv.has_slug(slg):
        slg = '-'.join([slug[:slug_length-len(str(i))-1], str(i)])
        i += 1

    sv.add_slug(slg)
    slug = slg
    if slug_postfix:
        slg = slug_postfix
        if slg == '$TimeStamp$':
            slg = datetime.now().strftime("%Y%m%d_%H%M%S")
        slug = '-'.join([slug[:slug_length-len(slg)], slg])
    return slug


def is_unique_filename(filename):
    i = 1
    while os.path.isfile(filename):
        dot = filename.rfind('.')
        file = filename[:dot]
        ext = filename[dot:]
        filename = ''.join([file, '-', str(i), ext])
        i += 1

    return filename


def is_number(s):
    if s is None:
        return False
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_integer(s):
    if s is None:
        return False
    try:
        n = float(s)
        m = n % 1
        if m > 0:
            return False
        else:
            return True
    except ValueError:
        return False


def is_date(s):
    if s is None:
        return False
    if isinstance(s, (datetime, date)):
        return True
    try:
        datetime.strptime(s, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def is_json(s):
    if s is None:
        return False
    if isinstance(s, dict):
        return True
    try:
        json.loads(s)
        return True
    except TypeError:
        return False
