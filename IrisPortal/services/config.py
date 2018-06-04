"""
    Config.py: Reads and writes configuration settings
    from and to the configuration file.
"""

from simplejson import dump, load
from sys import platform
from getpass import getuser

default_config = 'iris_portal.conf.json'

def _read_config(filename=default_config):
    with open(filename, 'rb') as f:
        result = load(f)
    return result


def _write_config(data, filename=default_config):
    with open(filename, 'wb') as f:
        dump(data, f)


# READ ONLY AREA

def get_capture_command(string=False, **kwargs):
    config = _read_config()
    cmd_ = config['video']['capturer']['cmd']
    cmd_conf = config['video']['capturer']['config']
    if string:
        cmd_str = ' '.join(cmd_)
        return cmd_str.format(**kwargs, **cmd_conf)
    cmd_list = []
    for i in cmd_:
        cmd_list.extend(i.split())
    return [
        i.format(**kwargs, **cmd_conf)
        for i in cmd_list
    ]


def get_stream_dir():
    config = _read_config()
    return config['locations']['stream']


def get_upload_dir():
    config = _read_config()
    return config['locations']['upload']


def get_devices_dir():
    config = _read_config()
    if 'media' in config['locations']:
        return config['locations']['media']
    if platform == 'linux' or platform == 'linux2':
        return '/media/{}/'.format(getuser())
    if platform == 'darwin':
        return '/Volumes/'


def get_uploader_location():
    config = _read_config()
    if 'upload' in config and 'location' in config['upload']:
        return config['upload']['location']
    else:
        return 'IrisRecordings'


def get_uploader_config():
    config = _read_config()
    if 'webdav' in config.get('upload', {}):
        return config['upload']['webdav']
    return None


def get_uploader_enabled():
    config = _read_config()
    if get_uploader_config():
        return config['upload'].get('enabled', False)
    return False


# READ/WRITE AREA

def set_capture_config(data):
    config = _read_config()
    config['video']['capturer']['config'] = data
    _write_config(config)


def get_cameras():
    config = _read_config()
    return config.get('video', {}).get('cameras', [])


def set_cameras(data):
    config = _read_config()
    config['video']['cameras'] = data
    _write_config(config)


def add_camera(**data):
    cameras = get_cameras()
    cameras.append(data)
    set_cameras(cameras)


def remove_camera(index):
    cameras = get_cameras()
    cameras.pop(index)
    set_cameras(cameras)

