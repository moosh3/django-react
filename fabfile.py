import os

# 3rd Party
from fabric.api import *
from contextlib import contextmanager

import fabtasks.development as dev
import fabtasks.production as prod
from fabtasks.context import virtualenv

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------

# Base env config
env.colorize_errors = True
env.package_name = 'Marjoram'
env.repository = 'https://github.com/marjoram/marjoram'
env.db_user = 'DB_USER'
env.db_name = 'DB_NAME'
env.virtualenv_dir = './venv/'
env.activate = 'source ./venv/bin/activate'
env.apache_restart_command = 'apache_restart'

# Local env
env.local_group = 'staff'
env.local_project_root = os.getcwd()
env.local_static_root = os.path.join(os.getcwd(), 'static_collection', '')
env.local_media_root = os.path.join(os.getcwd(), 'media', '')


@task
def production():
    """Production env overrides"""
    env.hosts = ['*']
    env.user = 'root'
    env.group = 'apache'
    env.domain = 'DOMAIN'
    env.project_root = '/var/www/vhosts/{domain}'.format(**env)
    env.static_root = '/var/www/vhosts/{domain}/static_collection/'.format(**env)
    env.media_root = '/var/www/vhosts/{domain}/media/'.format(**env)


# Set the default environment
production()

# -----------------------------------------------------------------------------
# Project specific
# -----------------------------------------------------------------------------

# Your code goes here
