from __future__ import unicode_literals
from flask import Flask, render_template, request, redirect, url_for, abort, session, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, VARCHAR
from jinja2 import Environment, PackageLoader
import pymysql.cursors
import os
import requests
import unittest
import requests
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


# CloudSQL & SQLAlchemy configuration
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
from sqlalchemy.ext.declarative import declarative_base
PROJECT_ID = 'vernal-bonfire-179320'
CLOUDSQL_USER = 'root'
CLOUDSQL_PASSWORD = 'admin'
CLOUDSQL_DATABASE = 'elevation_traffic'
CLOUDSQL_CONNECTION_NAME = 'vernal-bonfire-179320:us-central1:elevationgaming1'
e = create_engine('mysql+pymysql://{user}:{password}@130.211.122.176/{database}?unix_socket=/cloudsql/{connection_name}'.format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE, connection_name=CLOUDSQL_CONNECTION_NAME))
f = sessionmaker(bind = e)
s = scoped_session(f)
env = Environment(loader=PackageLoader('first', 'templates'))
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
Base = declarative_base()
WTF_CSR_ENABLED = True

class data_collection(Base):
    __tablename__ = 'entries'
    visitor_number = Column(Integer, primary_key=True)
    ip_address = Column(VARCHAR)
    
server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()

@app.route('/')
def index():
    return "Success"
    
@app.route('/info', methods=(['GET', 'POST']))
def post_info():
    error = None
    template = env.get_template('index.html')
    ip_address =  request.remote_addr
    
    ed_ip = data_collection(ip_address = ip_address)
    s.add(ed_ip)
    s.commit()

    if request.method == 'POST':
        fromaddr = 'elevationg4m1ng@gmail.com'
        toaddr = 'elevationg4m1ng@gmail.com'
        msg = MIMEMultipart()
        msg['From'] = request.form['email']
        body = request.form['message']
        sender = 'EMAIL:' + ' ' + request.form['email']
        name = 'FROM:' + ' ' + request.form['name']
        msg.attach(MIMEText(sender, 'plain'))
        msg.attach(MIMEText(name, 'plain'))
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(toaddr, "elevationgaming")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text, )
        server.quit()
        
    
    return template.render()



if __name__ == "__main__":
	app.run(host = '0.0.0.0')