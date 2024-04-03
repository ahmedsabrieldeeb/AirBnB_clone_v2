#!/usr/bin/python3
"""Generates a .tgz archive from the contents of the web_static folder"""

from fabric.api import env, run, put, local, task
from datetime import datetime
from os.path import exists

env.hosts = ['100.26.11.29', '18.204.20.248']


def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    if not exists(archive_path):
        print("Archive doesn't exist.")
        return False

    try:
        put(archive_path, '/tmp/')
        archive_filename = archive_path.split('/')[-1] \
            .split('.')[0]
        release_folder = '/data/web_static/releases/{}' \
            .format(archive_filename)
        run('sudo mkdir -p {}'.format(release_folder))
        run('sudo tar -xzf /tmp/{}.tgz -C {}'
            .format(archive_filename, release_folder))
        run('sudo rm /tmp/{}.tgz'.format(archive_filename))
        run('sudo rm /data/web_static/current')
        run('sudo ln -s {}/web_static /data/web_static/current'
            .format(release_folder))

        return True
    except Exception as e:
        print("An error occurred:", e)
        return False
