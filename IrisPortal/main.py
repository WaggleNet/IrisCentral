from services.vars import make_context
from flask import Flask
from workers.manager import managerProcess
from workers.logger import LoggerProcess
from sys import platform


app = Flask(__name__)

@app.route('/')
def app_main():
    global context
    return 'Current counter: {}'.format(context['status'].counter)


if __name__ == '__main__':
    if platform == 'win32':
        print('Sorry, IrisCentral does not support Windows.')
        exit(1)
    global context
    context = make_context()
    l = LoggerProcess(context)
    p = managerProcess(context)
    l.start()
    p.start()
    app.run()
    # Join the child processes
    p.join()
