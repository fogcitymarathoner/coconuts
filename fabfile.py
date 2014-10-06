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
INSTANCE_ID='i-d37496d9'

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
    cmd =  'rsync  -ah --delete  --exclude="*/tmp/*"   --exclude=".git/*"  %s marc@www.coconuts.sfblur.com:python_apps/coconuts'%(SRC)
    local(cmd)


def start():
    """
    start - start the AWS Packaging Server - run local
    :return:
    """
    local('aws ec2 start-instances --instance-ids %s'%(AWS_INSTANCE_ID))

def stop():
    """
    stop - stop the AWS Packaging Server - run local
    :return:
    """
    local('aws ec2 stop-instances --instance-ids %s'%(AWS_INSTANCE_ID))

def echo_ip():
    """
    echo_ip - report Public IP of AWS Packaging Server - run local
    :return:
    """
    ec2conn = connect_to_region('us-west-2',
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    reservations = ec2conn.get_all_instances()
    #print reservations.AWS_INSTANCE_ID

    instances = [i for r in reservations for i in r.instances]
    for i in instances:
        if i.id == AWS_INSTANCE_ID:
            pprint(i.ip_address)
