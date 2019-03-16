#!/usr/bin/env python3
# -*- coding:utf-8 -*-

### **************************************************************************** ###
# 
# Project: Snips Web Admin
# Created Date: Sunday, March 10th 2019, 1:45:08 pm
# Author: Greg
# -----
# Last Modified: Sat Mar 16 2019
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
from sqlalchemy import func,desc,extract,Date,cast
from models import Site, Mqttlog, SessionEndedReason, HermesComponent
from app import db
from datetime import datetime, timedelta
from sqlalchemy.types import TIME, DATE



class Overview(Resource):

    
    def get(self, daysbefore):

        steps = 1
        start = 0
        end = 24
        group_word = 'hour'

        filter_after = datetime.today() - timedelta(days = daysbefore)

        if daysbefore > 1:
            #days.. so between what days start/end
            steps = daysbefore
            start = filter_after.day
            group_word = 'day'


        def createGroupedArray(objArray, start, end, steps):
    
            newArray = []
            total = 0
            #print("objArray",objArray)
            if steps == 1:

                #putting the array into the hour order like 4pm - 3am
                hoursbefore = datetime.today() - timedelta(days = 1)
                if hoursbefore == 0:
                    hoursbefore = 23
                else:   
                    hoursbefore = hoursbefore.hour + 1
                    
                hoursnow = datetime.today().hour + 1
                
                for x in range(hoursbefore, 24, 1):
                    result = [element for element in objArray if element[1] == x]
                    if len(result) > 0:
                        #found
                        t = result[0][0]
                        total += t
                        newArray.append(t)
                    else:
                        newArray.append(0)
                for x in range(0, hoursnow, 1):
                    result = [element for element in objArray if element[1] == x]
                    if len(result) > 0:
                        #found
                        t = result[0][0]
                        total += t
                        newArray.append(t)
                    else:
                        newArray.append(0)

            else:
                #days looping
                j = 0
                thisDay = datetime.today() - timedelta(days = steps)
                while j <= steps:
                    result = [element for element in objArray if element[1] == thisDay.day
                                                            and element[2] == thisDay.month
                                                            and element[3] == thisDay.year]
                    if len(result) > 0:
                        #found
                        #print('found')
                        t = result[0][0]
                        total += t
                        newArray.append(t)
                    else:
                        #print('not found')
                        newArray.append(0)
                    thisDay = thisDay + timedelta(days = 1)
                    j+=1  
            return [total,newArray]
        
        ww_count = 0
        
        #graph chart of the top 10 intents in the db
        top10 = db.session.query(func.count(Mqttlog.id).label('count'), Mqttlog.hermesTopic ).\
                        filter(Mqttlog.hermes == HermesComponent.intent,Mqttlog.timestamp >= filter_after). \
                            group_by(Mqttlog.hermesTopic).order_by(desc('count')).limit(10).all()


        #filter the data from X till now to return only those records
        #filter_after = datetime.today() - timedelta(days = daysbefore)
        #rows = db.session.query(func.count(Mqttlog.id)).filter(Mqttlog.timestamp >= filter_after).count()
    

        #ww_count = db.session.query(db.func.count(Mqttlog.id)). \
        #            filter(Mqttlog.hermesTopic == 'detected',
        #                    Mqttlog.timestamp >= filter_after). \
        #                scalar()  #.filter(Services.dateAdd.between(start, end))
        ww_count = None
        if daysbefore > 1:
            ww_count = db.session.query(func.count(Mqttlog.id),extract(group_word,Mqttlog.timestamp),
                                                                extract('month',Mqttlog.timestamp),
                                                                extract('year',Mqttlog.timestamp)). \
                            filter(Mqttlog.hermesTopic == 'detected',
                                Mqttlog.timestamp >= filter_after). \
                            group_by(extract(group_word,Mqttlog.timestamp)).all()
        else:
            ww_count = db.session.query(func.count(Mqttlog.id),extract(group_word,Mqttlog.timestamp)). \
                            filter(Mqttlog.hermesTopic == 'detected',
                                Mqttlog.timestamp >= filter_after). \
                            group_by(extract(group_word,Mqttlog.timestamp)).all()



        intent_count = None
        if daysbefore > 1:
            intent_count = db.session.query(func.count(Mqttlog.id),extract(group_word,Mqttlog.timestamp),
                                                                extract('month',Mqttlog.timestamp),
                                                                extract('year',Mqttlog.timestamp)). \
                            filter(Mqttlog.hermes == HermesComponent.intent,
                                Mqttlog.timestamp >= filter_after). \
                            group_by(extract(group_word,Mqttlog.timestamp)).all()
        else:
            intent_count = db.session.query(func.count(Mqttlog.id),extract(group_word,Mqttlog.timestamp)). \
                            filter(Mqttlog.hermes == HermesComponent.intent,
                                Mqttlog.timestamp >= filter_after). \
                            group_by(extract(group_word,Mqttlog.timestamp)).all()


        intentNotRecognized_count = None
        if daysbefore > 1:
            intentNotRecognized_count = db.session.query(func.count(Mqttlog.id),extract(group_word,Mqttlog.timestamp),
                                                                extract('month',Mqttlog.timestamp),
                                                                extract('year',Mqttlog.timestamp)). \
                            filter(Mqttlog.hermesTopic == 'intentNotRecognized',
                                Mqttlog.timestamp >= filter_after). \
                            group_by(extract(group_word,Mqttlog.timestamp)).all()
        else:
            intentNotRecognized_count = db.session.query(func.count(Mqttlog.id),extract(group_word,Mqttlog.timestamp)). \
                            filter(Mqttlog.hermesTopic == 'intentNotRecognized',
                                Mqttlog.timestamp >= filter_after). \
                            group_by(extract(group_word,Mqttlog.timestamp)).all()

        error_count = None
        if daysbefore > 1:
            error_count = db.session.query(func.count(Mqttlog.id),extract(group_word,Mqttlog.timestamp),
                                                                extract('month',Mqttlog.timestamp),
                                                                extract('year',Mqttlog.timestamp)). \
                            filter(Mqttlog.termination == SessionEndedReason.error,
                                Mqttlog.timestamp >= filter_after). \
                            group_by(extract(group_word,Mqttlog.timestamp)).all()
        else:
            error_count = db.session.query(func.count(Mqttlog.id),extract(group_word,Mqttlog.timestamp)). \
                            filter(Mqttlog.termination == SessionEndedReason.error,
                                Mqttlog.timestamp >= filter_after). \
                            group_by(extract(group_word,Mqttlog.timestamp)).all()


        return {'wakeword': createGroupedArray(ww_count, start, end, steps),
                'intentsfound': createGroupedArray(intent_count, start, end, steps),
                'unknownintents': createGroupedArray(intentNotRecognized_count, start, end, steps),
                'errors': createGroupedArray(error_count, start, end, steps),
                'top10' : top10
        }


#add api to url links
api.add_resource(Overview, '/api/overview/<int:daysbefore>')

