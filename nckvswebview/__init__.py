# -*- coding: utf-8 -*-

from bottle import route, run, abort

from nckvsclient import KVSClient

_clients = {}


def get_client(datatype):
    if datatype not in _clients:
        client = KVSClient.from_file('nckvs-webview.ini')
        client.config['datatypename'] = datatype
        _clients[datatype] = client

    return _clients[datatype]


@route('/favicon.ico')
def favicon():
    return abort(404)


@route('/:datatype')
def search(datatype):
    client = get_client(datatype)
    return client.search([])


if __name__ == '__main__':
    run(host='0.0.0.0', port=9999)
