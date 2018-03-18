'''
make sure to install these packages on the linux system
$ sudo apt-get install libxml2-dev libxslt-dev python-dev
$ sudo apt-get install libcurl4-openssl-dev python-pycurl
$ sudo easy_install webdavclient

Only one file to upload in the ram disk
Replace test with real path names

Reminder: webdav cannot handle uploading more than 30 minutes! Limit file size
          Do NOT name the file the same! New ones will NOT be uploaded! (solution: enable the time stamp)
'''

import webdav.client as wc
import glob
import time
import datetime
import os

# login configurations
options = {
    'webdav_hostname': "https://dav.box.com/dav",
    'webdav_login':    "yuxuanc5@illinois.edu",
    'webdav_password': "ORDXFpwA1Z"
}
client = wc.Client(options)

# always check for files to upload
while True:
    # local path check
    file_list = glob.glob(os.getcwd() + '/test/*.txt')
    local_list = [os.path.basename(x) for x in file_list]

    if not(len(file_list)):
        continue

    '''
    # create a time stamp
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')
    '''

    # infinitely retry
    while not(client.check(remote_path='Test/' + local_list[0])):
        # sync upload file to remote path
        client.upload(remote_path='Test/' + local_list[0], local_path=file_list[0])

    os.remove(file_list[0])