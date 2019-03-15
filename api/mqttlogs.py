#!/usr/bin/env python3
# -*- coding:utf-8 -*-

### **************************************************************************** ###
# 
# Project: Snips Web Admin
# Created Date: Wednesday, March 13th 2019, 10:00:08 am
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




#from sqlalchemy.orm import aliased
from . import api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc, extract, Date, cast, or_, and_
from models import Site, Mqttlog, SessionEndedReason, HermesComponent, Slots
from app import db
#from datetime import datetime, timedelta
from sqlalchemy.types import TIME, DATE
import json
from sqlalchemy.orm import lazyload, aliased
from sqlalchemy.sql import text



class MqttLogView(Resource):

    
    def get(self, site_id, fromdate):
        #site_id = A = ALL Sites
        #site_id = "site name" only list for that site

        rows50 = []
        if site_id == 0:
            #rows50 = db.session.query(Mqttlog).options(lazyload('site')). \
            #                filter(Mqttlog.timestamp < fromdate). \
            #                order_by(desc(Mqttlog.id)).limit(21).all()
            rows50 = db.session.query(Mqttlog).options(lazyload('site')). \
                            filter(Mqttlog.timestamp < fromdate). \
                            order_by(desc(Mqttlog.timestamp)).limit(21).all()
        else:
            
            #selected_site_id = db.session.query(Site.id).filter(Site.name == site_id).first
            #selected_site = Site.query.filter_by(name = site_id).first()
            
            #if selected_site:
            #site_id = selected_site.id
            a = aliased(Mqttlog)
            b = aliased(Mqttlog)
            rows50 = db.session.query(a).distinct()
            rows50 = rows50.outerjoin(b, or_(a.sessionId == b.sessionId, a.sessionId == ''))
            rows50 = rows50.filter(((a.siteId == site_id) | (a.siteId == '') | (b.siteId == site_id) | (b.siteId == '')) & (a.timestamp < fromdate))
            rows50 = rows50.order_by(desc(a.timestamp)).limit(21).all()



        return_data = {'rows':[], "last_date":fromdate}

        

        if rows50:
            return_data = [ row.to_dict(rules=('fullhermes','terminationreason')) for row in rows50 ]
            
            
            return_data = {'rows':return_data, 
                            'last_date':str(rows50[len(rows50)-1].timestamp)}
        
        

        return return_data
        



#add api to url links
api.add_resource(MqttLogView, '/api/watch/<int:site_id>/<string:fromdate>')

