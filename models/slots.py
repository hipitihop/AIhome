#!/usr/bin/env python3
# -*- coding:utf-8 -*-

### **************************************************************************** ###
# 
# Project: Snips Web Admin
# Created Date: Wednesday, March 13th 2019, 8:53:15 am
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




from . import db, Site
from sqlalchemy import Table, Column, String, Integer, DateTime, ForeignKey, Boolean, func
from sqlalchemy_utils import ChoiceType
from flask_addins.serializer import SerializerMixin


class Slots(db.Model, SerializerMixin):

    serialize_only = ('id','rawValue','kind','value','entity','slotName','confidenceScore')  
    serialize_rules = ()

    __tablename__ = 'slots'
    id = Column(Integer, primary_key = True, autoincrement=True)
    mqttlog_id = Column(Integer, ForeignKey('mqttlog.id',ondelete='CASCADE'),nullable=True)
    

    rawValue = Column(String(255))
    kind = Column(String(100))
    value = Column(String(255))
    entity = Column(String(100))
    slotName = Column(String(100))
    confidenceScore = Column(Integer())


    def __repr__(self):
        return 'Slot Model' 

