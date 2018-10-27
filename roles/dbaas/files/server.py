#!/usr/bin/env python
# coding: utf-8
# __author__ = 'Benjamin'


import flask
from flask import request
import sqlalchemy


# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

app = flask.Flask(__name__)

# ------ DB params ------

db_host = 'localhost'
db_port = '3306'
db_user = 'service'
db_pwd = 'Servicep4ssword!'

MYSQL_URL='mysql+pymysql://{0}:{1}@{2}:{3}/'.format(db_user, db_pwd, db_host, db_port)

# engine = create_engine(MYSQL_URL)
# models.Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# conn = Session()

# ------ Web Server ------

@app.route('/', methods=['GET'])
def status():
    return flask.jsonify({  'service': 'db as a service',
                            'status': 'ok'})


@app.route('/db', methods=['GET', 'PUT', 'DELETE'])
def manage_db():
    engine = sqlalchemy.create_engine(MYSQL_URL)
    connect = engine.connect()
    
    # Get Databases
    if request.method == 'GET':
        db_list = connect.execute('show databases')
        return flask.jsonify({ 'db' : [{'name': item[0]} for item in db_list]})

    db_name = request.form.get('name')
    # Create Database
    if request.method == 'PUT':
        if db_name not in (None, 'db'):
            db = connect.execute('create database if not exists {}'.format(db_name))
    # Detele Database
    if request.method == 'DELETE':
        if db_name not in (None, 'db'):
            db = connect.execute('drop database if exists {}'.format(db_name))

    return flask.jsonify({ 'db' : {'name': db_name}})


@app.route('/<db_name>', methods=['GET', 'PUT', 'DELETE'])
def manage_table(db_name):
    try:
        engine = sqlalchemy.create_engine('{0}{1}'.format(MYSQL_URL, db_name))
        connect = engine.connect()
    except Exception as error:
        return flask.jsonify({'error': string(error)})

    # Get Tables
    if request.method == 'GET':
        table_list = engine.table_names()
        return flask.jsonify({ 'table': [{'name': item} for item in table_list]})

    table_name = request.form.get('name')
    # Create Table
    if request.method == 'PUT':
        table = connect.execute('create table {}'.format(table_name))    
    # Delete Table
    if request.method == 'DELETE':
        table = connect.execute('drop table {}'.format(table_name))

    return flask.jsonify({ 'table': {'name': table_name}}) 


# ------ Run Server ------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
