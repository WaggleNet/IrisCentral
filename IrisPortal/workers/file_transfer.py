from workers.base import contextualProcess
from time import sleep
from services.config import get_devices_dir
from configparser import RawConfigParser, NoSectionError
from pathlib import Path
from os import statvfs, path, remove
from humanfriendly import parse_size
from services.config import get_stream_dir
from shutil import copy2

class fileTransferProcess(contextualProcess):
    def __init__(self, context):
        super().__init__(context, 'FileTransfer')
        self.filecopy = self.context['filecopy']
        self.filecopy.drives = {}

    def probe_available_volumes(self):
        drives = self.filecopy.drives
        old_drives = set(drives.keys())
        visited = set()
        # First, scan all the drives for ones to add
        for i in Path(get_devices_dir()).glob('*'):
            try:
                conf_path = Path(i, 'iris_storage.conf')
                if i.is_dir() and conf_path.exists():
                    visited.add(str(i))
                    # If drive not exists, parse config and add
                    if str(i) not in drives:
                        p = RawConfigParser()
                        try:
                            self.logger.info('Found new drive at {}'.format(i))
                            Path(i, 'iris').mkdir(exist_ok=True)
                            p.read(conf_path)
                            disk_config = p.items('iris')
                            disk_config['status'] = 'active'
                            if 'space_limit' in disk_config:
                                disk_config['space_limit'] = parse_size(disk_config['space_limit'], binary=True)
                            else:
                                disk_config['space_limit'] = 0
                            self.logger.info('Successfully added drive {}.'.format(i))
                        except NoSectionError:
                            self.logger.info('{} missing config, had to infer capacity.'.format(i))
                            disk_config = {'status': 'active', 'space_limit': 0}
                    else:
                        disk_config = drives[str(i)]
                    fs_stat = statvfs(i)
                    disk_config['total_capacity'] = fs_stat.f_blocks * fs_stat.f_frsize
                    disk_config['free_space'] = fs_stat.f_bavail * fs_stat.f_frsize
                    drives[str(i)] = disk_config
            except Exception as e:
                self.logger.debug('Ignoring drive {} due to {}'.format(i, e.__repr__()))
        # Then clear up lost drives
        for i in old_drives - visited:
            if drives[str(i)]['status'] == 'active':
                self.logger.error('Drive {} abnormal detach.'.format(i))
            else:
                self.logger.info('Drive {} has been detached.'.format(i))
            drives.pop(i, 0)
        # Commit the changes
        self.filecopy.drives = drives

    def get_cadidate_drive(self, file_size):
        drives = self.filecopy.drives
        for k, v in drives.items():
            print(v)
            if v['status'] != 'active': continue
            if v['space_limit'] >= v['free_space'] - file_size:
                continue
            return k
        return None

    def run_file_copy(self):
        to_copy = ''
        try:
            stream_dir = get_stream_dir()
            available_files = []
            seg_lists = list(Path(stream_dir).glob('*_index.txt'))
            earliest_seg_ctime = None
            if seg_lists:
                earliest_seg_ctime = path.getctime(min(seg_lists, key=path.getctime))
                for i in seg_lists:
                    with open(i) as fp:
                        available_files.extend([
                            Path(stream_dir, j)
                            for j in fp.readlines() if j and Path(stream_dir, j).exists()
                        ])
            available_files.extend([
                j for j in Path(stream_dir).glob('*.mp4')
                if (path.getctime(j) < earliest_seg_ctime if earliest_seg_ctime else True)
            ])
            available_files.sort(key=path.getctime)
            if len(available_files) == 0:
                # self.logger.debug('Nothing to copy, quitting')
                return
            to_copy = available_files[0]
            candidate_drive = self.get_cadidate_drive(path.getsize(to_copy))
            self.logger.debug('Starting to copy {} to {}'.format(to_copy, candidate_drive))
            # Actually copy it
            copy2(to_copy, str(Path(candidate_drive, 'iris')))
            remove(to_copy)
            self.logger.debug('{} copied and deleted.'.format(to_copy))
        except Exception as e:
            self.logger.warning('Copy of {} failed due to error: {}'.format(to_copy, e.__repr__()))

    def run(self):
        self.logger.info('Started')
        try:
            while True:
                sleep(2)
                # Detect drives
                self.probe_available_volumes()
                drives = self.filecopy.drives
                # self.logger.debug('Drive probing ends. Found {} volumes'.format(len(drives)))
                # self.logger.debug(drives)
                # Copy file if ramdisk not empty
                self.run_file_copy()

        except (KeyboardInterrupt, SystemExit):
            return