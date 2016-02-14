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

@get('/trails/api/1/achievement')
def get_achievement():
    if not has_auth(request):
        response.status = 401
        return
    return {"achievements" :["the","internet","of","things"]}

def check_required_keys(dict, keys):
    for k in keys:
        if not k in dict:
            return False
    return True

def has_auth(request):
    return 'authtoken' in request.headers

run(host='localhost', port=8080)
