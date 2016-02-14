#!/usr/bin/env python
from bottle import route, run, template, request, post, get, response
import simplejson as json

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@post('/trails/api/1/login')
def login():
    if check_required_keys(request.json, ['email','password']):
        return {'authtoken': 'qwertyuiopasdfghjkl'}
    else:
        response.status = 400
        return

def check_required_keys(dict, keys):
    for k in keys:
        if not k in dict:
            return False
    return True

run(host='localhost', port=8080)
