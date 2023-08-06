# coding=utf-8

from urllib.parse import urlparse
import re


def url_parser(url: str) -> {}:
    parts = urlparse(url)
    resource = re.findall(r"[^\/]*$", parts.path)
    url_parts = {
        'protocol': parts.scheme,
        'domain': parts.netloc,
        'context_path': parts.path,
        'resource': resource[0]
    }
    parts = re.findall(r"^\d+", url_parts['resource'])
    if len(parts) > 0:
        url_parts['resource_id'] = int(parts[0])
    else:
        url_parts['resource_id'] = None
    return url_parts
