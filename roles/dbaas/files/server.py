#!/usr/bin/env python
# coding: utf-8
# __author__ = 'Benjamin'


import flask
from flask import request
import sqlalchemy
from sqlalchemy_utils import create_database, database_exists


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


@app.route('/db', methods=['GET'])
def read_db():
    engine = sqlalchemy.create_engine(MYSQL_URL)
    insp = sqlalchemy.inspect(engine)
    db_list = insp.get_schema_names()
    return flask.jsonify({ 'db' : [{'name': item} for item in db_list]})


@app.route('/db', methods=['POST'])
def create_db():
    db_name = request.args.get('name')
    if db_name not in (None, 'db'):
        if not database_exists(MYSQL_URL):
            create_database(db_name)
    return flask.jsonify({ 'db' : {'name': db_name}})


@app.route('/db', methods=['DELETE'])
def delete_db():
    db_name = request.args.get('name')
    if db_name not in (None, 'db'):
        if database_exists(MYSQL_URL):
            drop_database(db_name)
    return flask.jsonify({ 'db' : {'name': db_name}})


# ------ Run Server ------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
