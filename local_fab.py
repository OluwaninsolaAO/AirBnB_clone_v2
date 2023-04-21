#!/usr/bin/python3
"""
A Fabric script that generates a .tgz archive from the
contents of the web_static folder of AirBnB Clone repo, using
the function `do_pack`.

and does other stuffs.
"""

from fabric.api import local, env, run, put
from datetime import datetime
import os


def do_pack():
    """Compress the contents of web_static"""

    #  create `versions` dir if not exists
    local('sudo mkdir -p versions')

    #  create compressed tgz file
    time_stamp = datetime.now().strftime('%Y%m%d%H%M%S')
    path = 'versions/web_static_' + time_stamp + '.tgz'
    result = local('sudo tar -cvzf {} web_static/'.format(path))
    if result.succeeded:
        return path
    else:
        return None


def do_deploy(archive_path):
    """distributes an archive to env.hosts web servers"""

    #  if empty argument passed
    if not os.path.exists(archive_path):
        return False

    basename = os.path.basename(archive_path)
    path = basename.replace('.tgz', '')
    path = '/data/web_static/releases/{}'.format(path)

    #  upload archive to server
    local('sudo mv {} /tmp/'.format(archive_path))
    local('sudo mkdir -p {}'.format(path))
    local('sudo tar -xvzf /tmp/{} -C {}'.format(basename, path))
    local('sudo mv {}/web_static/* {}'.format(path, path))
    local('sudo rm -rf {}/web_static/'.format(path))
    local('sudo rm /data/web_static/current')
    local('sudo ln -s {} /data/web_static/current'.format(path))
    return True


def deploy():
    """creates and distributes an archive to web servers"""
    path = do_pack()
    if path is None:
        return False
    return do_deploy(path)


def do_clean(number=0):
    """ Deletes out-of-date archives."""

    #  check if path `versions/` exists
    if not os.path.exists('versions/'):
        return

    #  resolve least number of archives to keep
    if number == 0:
        number = 1

    #  capture list of archives : local
    archives = local('sudo ls -t versions/', capture=True)
    archives = archives.split('\n')

    archives = archives[int(number):]

    #  remove local archives
    for archive in archives:
        local('sudo rm versions/{}'.format(archive))

    #  capture list of archives : remote
    archives = local('sudo ls -t /data/web_static/releases')
    archives = archives.split('\n')

    archives = archives[int(number):]

    if 'test' in archives:
        archives.remove('test')

    for archive in archives:
        local('sudo rm -rf /data/web_static/releases/{}'.format(
            archive))
