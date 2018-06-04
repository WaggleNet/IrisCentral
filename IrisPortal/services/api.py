def get_drives(c):
    drives = c['filecopy'].drives
    return [{'id': k, **v} for k, v in drives.items()]


def get_cameras(c):
    cameras = c['streams'].status
    return list(cameras.values())


def eject_drive(c, drive_id):
    drives = c['filecopy'].drives
    drives[drive_id]['status'] = 'ejected'
    c['filecopy'].drives = drives


def get_uploader_status(c):
    uploader_ns = c['uploader']
    if uploader_ns.enabled:
        result = {
            'enabled': True,
            'active': uploader_ns.active
        }
    else:
        result = {
            'enabled': False
        }
    result['config'] = {**uploader_ns.config}
    return result


def set_uploader_config(c, form):
    uploader_ns = c['uploader']
    assert 'hostname' in form
    assert 'username' in form
    assert 'password' in form
    assert 'location' in form
    uploader_ns.config = form
    uploader_ns.enabled = True


def disable_uploader(c):
    uploader_ns = c['uploader']
    uploader_ns.enabled = False