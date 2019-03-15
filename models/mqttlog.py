#!/usr/bin/env python3
# -*- coding:utf-8 -*-

### **************************************************************************** ###
# 
# Project: Snips Web Admin
# Created Date: Saturday, March 9th 2019, 8:39:33 pm
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




from . import db, Site
import datetime
from sqlalchemy import Table, Column, String, Integer, DateTime, ForeignKey, Boolean, func
from enum import Enum
from sqlalchemy_utils import ChoiceType
from sqlalchemy.orm import relationship, backref
from flask_addins.serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property


class HermesComponent(Enum):
    dialogueManager = 1
    nlu = 2
    tts = 3
    hotword = 4
    asr = 5
    error = 6
    intent = 7
    audioServer = 8

HermesComponent.dialogueManager.label = u'Dialogue Manager'
HermesComponent.nlu.label = u'NLU'
HermesComponent.tts.label = u'TTS'
HermesComponent.hotword.label = u'Hotword'
HermesComponent.asr.label = u'ASR'
HermesComponent.error.label = u'Error'
HermesComponent.intent.label = u'Intent'
HermesComponent.audioServer.label = u'Audio Server'


class SessionEndedReason(Enum):
    nominal = 1
    abortedByUser = 2
    intentNotRecognized = 3
    timeout = 4
    error = 5

SessionEndedReason.nominal.label = u'Nominal'
SessionEndedReason.abortedByUser.label = u'Aborted by user'
SessionEndedReason.intentNotRecognized.label = u'Intent not recognized'
SessionEndedReason.timeout.label = u'Timeout'
SessionEndedReason.error.label = u'Error'




class Mqttlog(db.Model, SerializerMixin):

    serialize_only = ()   # Define custom schema here if needed
    serialize_rules = ()#('-slots_id.mqttlog_id')  # Define custom schema here if needed

    datetime_format = '%Y-%m-%d %H:%M:%S.%f'

    __tablename__ = 'mqttlog'
    id = Column(Integer, primary_key = True, autoincrement=True)
    #siteId = Column(Integer, ForeignKey('site.id'))
    siteId = Column(Integer, ForeignKey('site.id',ondelete='CASCADE'),nullable=True)
    slots_id = relationship("Slots", backref=backref("mqttlog", lazy="joined"), cascade="all, delete")
    timestamp = Column(DateTime, default=datetime.datetime.now)
    hermes = Column(ChoiceType(HermesComponent, impl=Integer()))
    hermesTopic = Column(String(50))
    #sessiontype = Column(ChoiceType(DialogueManagerSessions, impl=Integer()))
    termination = Column(ChoiceType(SessionEndedReason, impl=Integer()))
    terminationerror = Column(String(255))
    sessionId = Column(String(36))
    reactivatedFromSessionId = Column(String(36))
    customData = Column(String(50))
    text = Column(String(50))
    intentFilter = Column(String(50))
    startsessiontype = Column(String(15))
    intent = Column(String(50))
    confidenceScore = Column(Integer())
    intentinput = Column(String(50))
    modelId = Column(String(50))
    error = Column(String(255))
    context = Column(String(255))
    canBeEnqueued = Column(Boolean)
    sendIntentNotRecognized = Column(Boolean)



    def __repr__(self):
        return 'MQTT LOG Model' 

    @hybrid_property
    def fullhermes(self):
        return self.hermes.label

    @hybrid_property
    def terminationreason(self):
        if self.termination:
            return self.termination.label
        
        return ''


    
