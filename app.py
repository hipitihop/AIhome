#!/usr/bin/env python3
# -*- coding:utf-8 -*-

### **************************************************************************** ###
# 
# Project: Snips Web Admin
# Created Date: Friday, March 8th 2019, 4:43:06 pm
# Author: Greg
# -----
# Last Modified: Fri Mar 15 2019
# Modified By: Greg
# -----
# Copyright (c) 2019 Greg
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
# AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 
### **************************************************************************** ###




from flask import Flask, url_for, render_template
from flask_migrate import Migrate
from flask_security import Security, login_required, SQLAlchemyUserDatastore
from flask_admin import helpers as admin_helpers
from flask_security.utils import encrypt_password
from sqlalchemy_utils import database_exists
from models import db, Role, User,Mqttlog
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import click








#============================================================== 
# Error page routes 
#==============================================================

def page_not_found(e):
  return render_template('error/pages-error-404.html'), 404

def page_not_found_400(e):
  return render_template('error/pages-error-400.html'), 400

def page_forbiddon(e):
  return render_template('error/pages-error-403.html'), 403

def page_server_error(e):
  return render_template('error/pages-error-500.html'), 500

def page_service_unavailable(e):
  return render_template('error/pages-error-503.html'), 503

#============================================================== 
# FLASK
#==============================================================

app = Flask(__name__)
app.config.from_pyfile('config.py')


app.url_map.strict_slashes = False

#register page error handling to display a page error
app.register_error_handler(400, page_not_found_400)
app.register_error_handler(403, page_forbiddon)
app.register_error_handler(404, page_not_found)
app.register_error_handler(500, page_server_error)
app.register_error_handler(503, page_service_unavailable)

#with app.app_context():
db.init_app(app)
db.app = app

def init_objects(app):
  from api import api
  #with app.app_context():
  api.init_app(app)
  api.app = app

  from service.mqttService import mqtt
  #with app.app_context():
  mqtt.init_app(app)
  mqtt.app = app


migrate = Migrate(app, db)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

security = Security(app, user_datastore)

#============================================================== 
# CRON job
#==============================================================

#every day delete older than 30 days of records
#to keep db small and fast
#who really cares about anything older than 30 days ago?? really?!??!
def clean_db():
    since = datetime.now() - timedelta(days=30)
    sq = db.session.query(Mqttlog).filter(Mqttlog.timestamp < since).all()
    for row in sq:
        db.session.delete(Mqttlog.query.get(row.id))
        db.session.flush()
    
    db.session.commit()
    

#run every day @ 4:12am
sched = BackgroundScheduler(daemon=True)
sched.add_job(clean_db, trigger='cron', hour='04', minute='12')
sched.start()


# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: sched.shutdown(wait=False))


#============================================================== 
# App Routes 
#==============================================================

@app.route("/")
@login_required
def dashboard_overview():
  bar = {"title":"Dashboard","link":"Overview"}
  return render_template('index.html',bar=bar,includeJS="overview")

@app.route("/watch")
@login_required
def watch_log_viewer():
    bar = {"title":"Dashboard","link":"Watch Log","link":"Timeline"}
    return render_template('watch.html',bar=bar,includeJS="watch")


#============================================================== 
# CLI and Generate new DB
#==============================================================

@app.cli.command()
@click.argument('password')
def set_password(password):
  with app.app_context():
    admin_user = user_datastore.get_user(1)
    if (admin_user):
      admin_user.password = encrypt_password(password)
      db.session.commit()


#if there is no DB create it and setup default data
if not database_exists(db.engine.url):
    db.create_all()
    #create admin/admin default account
    with app.app_context():
      super_admin_role = Role(name = 'superadmin')
      admin_role = Role(name = 'admin')
      db.session.add(super_admin_role)
      db.session.add(admin_role)
      db.session.commit()

      admin_user = user_datastore.create_user(
        email = 'admin',
        password = encrypt_password('admin'),
        roles = [super_admin_role, admin_role]
      )
      db.session.add(admin_user)
      db.session.commit()
  
#now create the api and mqtt services etc
init_objects(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    #app.run()
