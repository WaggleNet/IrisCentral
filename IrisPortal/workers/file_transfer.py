from workers.base import contextualProcess
from time import sleep
from services.config import get_devices_dir
from pathlib import Path

class fileTransferProcess(contextualProcess):
    def __init__(self, context):
        super().__init__(context, 'FileTransfer')
        self.context['status'].counter = 0

    @staticmethod
    def probe_available_volumes():
        results = []
        for i in Path(get_devices_dir()).glob('*'):
            try:
                if i.is_dir() and Path(i, 'iris_storage.conf').exists():
                    results.append(i)
            except:
                pass
        return results

    def run(self):
        self.logger.info('Started')
        try:
            while True:
                sleep(2)
                volumes = self.probe_available_volumes()
                self.logger.info('Found {} volumes: {}'.format(len(volumes), volumes))
        except (KeyboardInterrupt, SystemExit):
            return