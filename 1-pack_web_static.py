#!/usr/bin/env python3
"""A Fabric script that generates a .tgz archive from the
contents of the web_static folder of AirBnB Clone repo, using
the function `do_pack`."""

from fabric.api import local
from datetime import datetime


def do_pack():
    """Compress the contents of web_static"""

    local('mkdir -p versions')
    time_stamp = datetime.now().strftime('%Y%m%d%H%M%S')
    path = 'versions/web_static_' + time_stamp + '.tgz'
    result = local('tar -cvzf {} web_static/'.format(path))
    if result.succeeded:
        return path
    else:
        return None
