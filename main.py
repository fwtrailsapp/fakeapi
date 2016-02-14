#!/usr/bin/python
from bottle import route, run, template, request, post, get, response
import MySQLdb
import simplejson as json

'''
Place this file in Library/WebServer/Documents and execute it there.
This automatically sets up a web server that listens on port 8080.
'''

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)


@get('/trails/account')
def get_user():
    email = request.query.email
    cursor.execute("select * from account where PK_EMAIL='{}'".format(email))
    user = cursor.fetchone()
    response.set_header('Content-Type', 'application/json')
    user_dict = {}
    user_dict['email'] = user[0]
    user_dict['password'] = user[1]
    user_dict['first_name'] = user[2]
    user_dict['last_name'] = user[3]
    user_dict['age'] = user[4]
    user_dict['weight'] = json.dumps(user[5])
    user_dict['sex'] = user[6]
    user_dict['height'] = json.dumps(user[7])  

    return user_dict 

@post('/trails/add_account')
def add_user():
    request_json = request.json
    
    print type(request_json)

    values = ''
    keys = ''
    first = True        

    for key in request_json:
        if first == True:
            values += str(request_json[key])
            keys += str(key)
            first = False
        else:
            keys += ',' + str(key)
            values += ',' + str(request_json[key])
    
    print 'insert into ACCOUNT (' + keys + ') values (' + values + ');'
    cursor.execute('insert into ACCOUNT (' + keys + ') values (' + values + ');')
    trails_db.commit()


@post('/trails/api/1/activity')
def create_activity():
    
    request_json = request.json

    values = ''
    keys = ''
    first = True  

    for key in request_json:
        if first == True:
            values += str(request_json[key])
            keys += str(key)
            first = False
        else:
            keys += ',' + str(key)
            values += ',' + str(request_json[key]) 
    print 'insert into ACTIVITY (' + keys + ') values (' + values + ');'
    cursor.execute('insert into ACTIVITY (' + keys + ') values (' + values + ');')
    trails_db.commit()


trails_db = MySQLdb.connect(host="localhost", user="root", passwd="", db="trails")
cursor = trails_db.cursor()

run(host='localhost', port=8080)
