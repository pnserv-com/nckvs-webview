# -*- coding: utf-8 -*-

import os

import bottle
bottle.TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__),
                                         'templates'))

from bottle import route, run, abort, view

from nckvsclient import KVSClient

try:
    from configparser import ConfigParser
except:
    from ConfigParser import SafeConfigParser as ConfigParser

_clients = {}
_datatypes = []


def get_client(datatype):
    if datatype not in _clients:
        client = KVSClient.from_file('nckvs-webview.ini')
        client.config['datatypename'] = datatype
        _clients[datatype] = client

    return _clients[datatype]


@route('/')
@view('index')
def index():
    return dict(datatypes=_datatypes)


@route('/favicon.ico')
def favicon():
    return abort(404)


@route('/:datatype')
def search(datatype):
    client = get_client(datatype)
    return client.search([])


if __name__ == '__main__':
    parser = ConfigParser()
    parser.read('nckvs-webview.ini')
    datatypes = parser.get('webview', 'datatypes')
    _datatypes.extend(x.strip() for x in datatypes.split(','))
    run(host='0.0.0.0', port=9999)
