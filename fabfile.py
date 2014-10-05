__author__ = 'marc'
import os
from fabric.api import run
from fabric.api import get
from fabric.api import local
from fabric.api import settings
import json

from pprint import pprint

import boto
from boto.ec2 import connect_to_region
from datetime import datetime


from local_settings import AWS_ACCESS_KEY_ID
from local_settings import AWS_SECRET_ACCESS_KEY


now = datetime.now()


RSYNC_ARGS = '-vrz  --delete --exclude=*.pyc'

SRC = '/home/marc/python_apps/coconuts/'
DEST = 'www'
AWS_INSTANCE_ID = 'i-1578a51a'


IDEA_ZIP_FILE = 'tmp/idea.tar.bz2'
IDEA_DIR = '.idea'


BUCKET_NAME = 'alsdkfadomsdfjfj'

def sync():
    """
    copy local changes in ~/personal/chef to sfgeek.net:rails_apps/rrg_chef using rsync
    :return:
    """
    cmd =  'rsync -ah --delete  --exclude="*/tmp/*"   --exclude=".git/*"  %s marc@sfgeek.net:python_apps/coconuts'%(SRC)
    local(cmd)

