from workers.base import contextualProcess
from time import sleep


class fileTransferProcess(contextualProcess):
    def __init__(self, context):
        super().__init__(context, 'FileTransfer')
        self.context['status'].counter = 0

    def run(self):
        self.logger.info('Started')
        try:
            while True:
                sleep(2)
        except (KeyboardInterrupt, SystemExit):
            return