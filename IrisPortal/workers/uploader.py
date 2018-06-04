from workers.base import contextualProcess
from time import sleep
from services.config import get_upload_dir, get_uploader_config, get_uploader_location, get_uploader_enabled
from pathlib import Path
from os import statvfs, path, remove
from shutil import copy2
from webdav.client import Client


class uploaderProcess(contextualProcess):
    def __init__(self, context):
        super().__init__(context, 'Uploader')
        self.uploader = self.context['uploader']
        self.filecopy = self.context['filecopy']
        self.uploader.config = {
            **(get_uploader_config() or {'hostname': '', 'username': '', 'password': ''}),
            'location': get_uploader_location()
        }
        self.uploader.enabled = get_uploader_enabled()
        self.uploader.active = False
        self.client = None

    def init_client(self):
        try:
            conf = self.uploader.config
            self.client = Client({
                'webdav_hostname': conf['hostname'],
                'webdav_password': conf['password'],
                'webdav_login': conf['username']
            })
            if not self.client.check(self.uploader.config['location']):
                raise FileNotFoundError('Location not found, giving up')
            self.uploader.active = True
            self.logger.info('Uplink established')
        except Exception as e:
            self.logger.error('Failed to establish uplink, reason, {}'.format(e.__repr__()))

    def find_available_files(self):
        for loc, config in self.filecopy.drives.items():
            try:
                assert config['status'] == 'active'
                files = list(Path(loc, 'iris').glob('*.mp4'))
                assert len(files) > 1
                candidate = min(files, key=path.getctime)
                return candidate
            except AssertionError:
                pass
            except Exception as e:
                self.logger.warning('Skipping disk probing {} due to '.format(loc, e.__repr__()))
        return None

    def run_upload(self, filepath):
        """
        Actually run the upload.
        :param filepath: File path.
        :type filepath: Path or str
        :return: None
        :rtype: NoneType
        """
        destination = get_upload_dir()
        uploadPath = self.uploader.config['location']
        new_path = Path(destination, filepath)
        copy2(filepath, destination)
        self.client.upload_sync(
            remote_path=uploadPath+Path(filepath).name,
            local_path=new_path
        )
        remove(str(new_path))
        remove(str(filepath))
        self.logger.info('File {} uploaded and cleared'.format(uploadPath))


    def run(self):
        self.logger.info('Started')
        try:
            while True:
                sleep(5)
                # Establish connection if enabled
                if not self.uploader.active:
                    if self.uploader.enabled:
                        self.init_client()
                else:
                    # Start looking for files to upload
                    file = self.find_available_files()
                    if file:
                        try:
                            self.logger.info('Trying to upload file {}'.format(file))
                            self.run_upload(file)
                        except Exception as e:
                            self.logger.error('Uploader error {}, forcing offline'.format(e.__repr__()))
                            self.uploader.active = False
                            self.client = None
                    if not self.uploader.enabled:
                        self.uploader.active = False
                        self.logger.info('Uplink disabled, service ends')
        except (KeyboardInterrupt, SystemExit):
            return