from multiprocessing import Process
from services.logging import QueueHandler
from logging import getLogger, DEBUG


class contextualProcess(Process):
    def __init__(self, context, name=__name__):
        super().__init__()
        self.context = context
        h = QueueHandler(context['logs'])
        self.logger = getLogger(name)
        if not self.logger.handlers:
            self.logger.addHandler(h)
            self.logger.setLevel(DEBUG)
