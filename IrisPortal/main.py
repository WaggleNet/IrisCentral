from services.vars import make_context
from flask import Flask, render_template, jsonify, request
from workers.manager import managerProcess
from workers.logger import LoggerProcess
from sys import platform
from services.api import *
import logging


app = Flask(__name__)

@app.route('/')
def app_main():
    return render_template('index.html')

@app.route('/api/drives')
def api_get_drives():
    global context
    return jsonify(get_drives(context))


@app.route('/api/cameras')
def api_get_cameras():
    global context
    return jsonify(get_cameras(context))


@app.route('/api/eject')
def api_eject_drive():
    global context
    try:
        drive_id = request.args['id']
        eject_drive(context, drive_id)
        return jsonify(status='ok')
    except Exception as e:
        return jsonify(status='error', msg=e.__repr__())


@app.route('/api/uploader')
def api_get_uploader():
    global context
    return jsonify(get_uploader_status(context))


@app.route('/api/uploader/set', methods=['GET', 'POST'])
def api_set_uploader():
    global context
    set_uploader_config(context, request.json or request.form.to_dict())
    return jsonify(status='ok')


@app.route('/api/uploader/disable')
def api_disable_uploader():
    global context
    disable_uploader(context)
    return jsonify(status='ok')


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
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run()
    # Join the child processes
    p.join()
