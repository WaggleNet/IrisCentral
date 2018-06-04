from workers.base import contextualProcess
from workers.capture import capturerProcess
from workers.file_transfer import fileTransferProcess
from workers.uploader import uploaderProcess
from time import sleep


class managerProcess(contextualProcess):
    def __init__(self, context):
        super().__init__(context, 'Manager')
        self.jobs = {
            "capturer": capturerProcess,
            "transfer": fileTransferProcess,
            "uploader": uploaderProcess
        }
        self.workers = {}

    def start_job(self, k):
        self.workers[k] = self.jobs[k](self.context)
        self.workers[k].daemon = True
        self.workers[k].start()

    def run(self):
        self.logger.info('Manager has started')
        # Start bringing up the processes
        for k in self.jobs.keys():
            self.start_job(k)
        try:
            while True:
                for k, p in self.workers.items():
                    if not p.is_alive():
                        self.logger.warning('[{}] exited with code {}, restarting.'.format(k, p.exitcode))
                        self.start_job(k)
                sleep(1)
        except (KeyboardInterrupt, SystemExit):
            for p in self.workers.values():
                if p.is_alive():
                    p.terminate()
            return