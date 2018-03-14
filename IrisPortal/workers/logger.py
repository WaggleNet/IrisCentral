from workers.base import contextualProcess
from logging import StreamHandler, getLogger, DEBUG, Formatter
from coloredlogs import install
from sys import stderr


class LoggerProcess(contextualProcess):
    def run(self):
        q = self.context['logs']
        out_logger = getLogger('stdout')
        out_logger.setLevel(DEBUG)
        # ch = StreamHandler(stderr)
        # formatter = Formatter('%(asctime)s %(levelname)s [%(name)s] %(message)s')
        # ch.setFormatter(formatter)
        # out_logger.addHandler(ch)
        install(
            level='DEBUG',
            logger=out_logger,
            fmt='%(asctime)s %(levelname)s %(name)s %(message)s',
            datefmt='%H:%M:%S'
        )
        while True:
            try:
                record = q.get()
                if record is None:
                    break
                out_logger.handle(record)
            except (KeyboardInterrupt, SystemExit):
                return
            except Exception as e:
                print(e)