#!/usr/bin/env python3
# -*- coding:utf-8 -*-

### **************************************************************************** ###
# 
# Project: Snips Web Admin
# Created Date: Saturday, March 9th 2019, 2:15:14 pm
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




from . import db
from sqlalchemy import Column, String, Integer
from flask_addins.serializer import SerializerMixin
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property


class Site(db.Model, SerializerMixin):
    serialize_only = ('id','name') 
    serialize_rules = ()

    __tablename__ = 'site'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False)
    mqttlog_id = relationship("Mqttlog", backref=backref("site", lazy="joined"), cascade="all, delete")


    def __repr__(self):
        return '{}'.format(self.name) 

    @hybrid_property
    def fullsitename(self):
        return self.site.name

