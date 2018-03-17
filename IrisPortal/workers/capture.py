from workers.base import contextualProcess
from services.config import get_cameras, get_stream_dir, get_capture_command
from time import sleep
from pathlib import Path
from subprocess import Popen, DEVNULL


class capturerProcess(contextualProcess):
    def __init__(self, context):
        super().__init__(context, 'Capturer')
        self.streams = self.context['streams']
        self.configLock = self.context['configLock']
        self.processes = {}

    def make_dir(self):
        try:
            self.configLock.acquire()
            stdir = get_stream_dir()
            Path(stdir).mkdir(parents=True, exist_ok=True)
        finally:
            self.configLock.release()
        return stdir

    def load_streams(self):
        # Fetch the stream list from settings
        streams = self.streams
        try:
            self.configLock.acquire()
            status = get_cameras()
            st_dir = get_stream_dir()
            for i in status:
                i['capture_cmd'] = get_capture_command(
                    directory=st_dir,
                    camera_id=i['id'],
                    url=i['url']
                )
                i['status'] = 'pending'
            status = {i['id']: i for i in status}
            streams.status = status
        finally:
            self.configLock.release()

    def start_stream(self, k):
        self.logger.info('Starting capture for {}'.format(k))
        streams_ = self.streams.status
        cmd_ = streams_[k]['capture_cmd']
        self.logger.debug('Executing {}'.format(cmd_))
        self.processes[k] = Popen(cmd_, stderr=DEVNULL, stdout=DEVNULL)
        # self.processes[k] = Popen(cmd_)
        streams_[k]['status'] = 'running'
        self.streams.status = streams_

    def stop_stream(self, k):
        self.logger.info('Terminating capturer {}'.format(k))
        streams_ = self.streams.status
        if k in self.processes and self.processes[k].poll():
            self.processes[k].terminate()
            streams_[k]['status'] = 'terminated'
        self.streams.status = streams_

    def run(self):
        self.logger.info('Started.')
        self.logger.debug('Creating stream directory.')
        self.logger.debug('Stream dir created: {}'.format(self.make_dir()))
        self.logger.info('Loading camera streams.')
        self.load_streams()
        self.logger.debug(
            "Loaded {} streams: {}".format(
                len(self.streams.status),
                '; '.join(i for i in self.streams.status)
            )
        )
        self.logger.info('Starting to spawn capturers.')
        try:
            while True:
                sleep(2)
                streams_ = self.streams.status
                for k, v in streams_.items():
                    if v['status'] == 'running':
                        # Poll the stream
                        if (not self.processes[k]) or (self.processes[k].poll()):
                            # Process has terminated
                            v['status'] = 'dead'
                            exitcode = self.processes[k].poll()
                            if exitcode == 0:
                                self.logger.error('Capturer for {} terminated normally.'.format(k))
                            else:
                                self.logger.error('Capturer for {} abnormal exit with code {}.'.format(k, exitcode))
                            self.streams.status = streams_
                    else:
                        # Bring up the process
                        self.start_stream(k)
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            for k in self.streams.status:
                self.stop_stream(k)