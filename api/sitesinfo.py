#!/usr/bin/env python3
# -*- coding:utf-8 -*-

### **************************************************************************** ###
# 
# Project: Snips Web Admin
# Created Date: Wednesday, March 13th 2019, 9:20:53 pm
# Author: Greg
# -----
# Last Modified: Wed Mar 13 2019
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
from models import Site
from app import db




class SitesInfo(Resource):

    
    def get(self):
        #site_id = A = ALL Sites
        #site_id = "site name" only list for that site
        sites = db.session.query(Site).all()

        returnDict={}
        if len(sites) > 0:
            returnDict = [ row.to_dict() for row in sites ]


        return returnDict
        



#add api to url links
api.add_resource(SitesInfo, '/api/sites')