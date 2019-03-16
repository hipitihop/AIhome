#!/usr/bin/env python3
# -*- coding:utf-8 -*-

### **************************************************************************** ###
# 
# Project: Snips Web Admin
# Created Date: Friday, March 15th 2019, 10:01:38 pm
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




from . import api, Resource
import json
from subprocess import Popen, PIPE


class Services(Resource):

    
    def get(self):

        #set all to off
        status = {"hotword":0,"nlu":0,"asr":0,"tts":0,"dialogue":0,"skillserver":0,"audioserver":0}

        cmd = "ps ax | grep -v grep | grep 'snips-*'"
        p = Popen(cmd , shell=True, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        if p.returncode == 0:
            if not err:
                s = out.decode('utf-8').rstrip()
                if 'snips-hotword' in s:
                    status['hotword'] = 1
                if 'snips-asr' in s:
                    status['asr'] = 1
                if 'snips-nlu' in s:
                    status['nlu'] = 1
                if 'snips-dialogue' in s:
                    status['dialogue'] = 1
                if 'snips-tts' in s:
                    status['tts'] = 1
                if 'snips-skill-server' in s:
                    status['skillserver'] = 1
                if 'snips-audio-server' in s:
                    status['audioserver'] = 1

        return status


api.add_resource(Services, '/api/services')