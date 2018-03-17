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