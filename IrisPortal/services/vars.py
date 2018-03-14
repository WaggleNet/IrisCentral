"""
    Vars: Provides manager for ephemoral configuration data.
"""

from multiprocessing import Manager


def make_context():
    manager = Manager()
    context = {
        'status':  manager.Namespace(),
        'configLock': manager.Lock(),
        'streams': manager.Namespace(),
        'capturer': manager.Namespace(),
        'logs': manager.Queue()
    }
    return context
