#!/usr/bin/env python3
# -*- coding:utf-8 -*-

### **************************************************************************** ###
# 
# Project: Snips Web Admin
# Created Date: Sunday, March 10th 2019, 3:45:18 pm
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




from flask_mqtt import Mqtt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import Site
from models import Mqttlog, SessionEndedReason, HermesComponent, Slots
import json
from app import db



mqtt = Mqtt()

devices = {}

def loadSiteDictionary():
    result = db.session.query(Site.id,Site.name).all()
    for site in result:
        devices[site.name] = site.id


#build the device site list on start
loadSiteDictionary()

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.unsubscribe_all()
    """mqtt.subscribe('hermes/tts/say')
    #mqtt.subscribe('hermes/feedback/sound/toggleOff')
    #mqtt.subscribe('hermes/feedback/sound/toggleOn')"""
    mqtt.subscribe('hermes/audioServer/+/playFinished')
    mqtt.subscribe('hermes/audioServer/+/playBytes/#')
    mqtt.subscribe('hermes/dialogueManager/startSession')
    mqtt.subscribe('hermes/dialogueManager/sessionQueued')
    mqtt.subscribe('hermes/dialogueManager/continueSession')
    mqtt.subscribe('hermes/dialogueManager/endSession')
    mqtt.subscribe('hermes/dialogueManager/sessionEnded')
    mqtt.subscribe('hermes/dialogueManager/sessionStarted')
    mqtt.subscribe('hermes/intent/#')
    mqtt.subscribe('hermes/nlu/intentNotRecognized')
    #mqtt.subscribe('hermes/nlu/intentParsed') - not for production
    #mqtt.subscribe('hermes/nlu/query')
    mqtt.subscribe('hermes/nlu/slotParsed')
    mqtt.subscribe('hermes/error/nlu')
    mqtt.subscribe("hermes/asr/textCaptured")
    #mqtt.subscribe("hermes/asr/partialTextCaptured") - pointless db'ing this
    mqtt.subscribe("hermes/asr/startListening")
    mqtt.subscribe("hermes/asr/stopListening")
    mqtt.subscribe("hermes/hotword/+/detected")
    mqtt.subscribe("hermes/hotword/toggleOn")
    mqtt.subscribe("hermes/hotword/toggleOff")



@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    #print("message.topic",message.topic)
    #print("message.payload",message.payload)

    dic = {}
    topic = message.topic
    topicEnding = topic.split("/")
    payload = None

    ##################################################################
    ##     Audio Server                                             ##
    ##################################################################
    if 'hermes/audioServer/' in topic:
        #payload could be just a wav data so we dont load payload here at all
        try:
            dic['siteId'] = topicEnding[2] #contains siteid
            dic['hermesTopic'] = topicEnding[3]

            if topicEnding[3] == 'playFinished':
                temppayload = json.loads(message.payload.decode('utf-8'))
                if 'sessionId' in temppayload:
                    dic['sessionId'] = temppayload['sessionId']

            dic["hermes"] = HermesComponent.audioServer.value
            
        except Exception as e:
            print("ERROR: mqtt.on_message - AudioServer {}:".format(topicEnding[3]), e)

    else:

        #these items in here have a payload

        payload = json.loads(message.payload.decode('utf-8'))
        topicEnding = topicEnding[len(topicEnding)-1]

        ##################################################################
        ##     Hotword                                                  ##
        ##################################################################
        if 'hermes/hotword/' in topic:
            try:
                dic = {"hermes":HermesComponent.hotword.value,"hermesTopic":topicEnding}
            except Exception as e:
                print("ERROR: mqtt.on_message - Hotword {}:".format(topicEnding), e)
        
        ##################################################################
        ##     ASR                                                      ##
        ##################################################################
        elif 'hermes/asr/' in topic:
            try:
                dic = {"hermes":HermesComponent.asr.value,"hermesTopic":topicEnding}
            except Exception as e:
                print("ERROR: mqtt.on_message ASR {}:".format(topicEnding), e)

        ##################################################################
        ##     ERROR / NLU                                              ##
        ##################################################################
        elif 'hermes/error/' in topic:
            try:
                dic = {"hermes":HermesComponent.error.value,"hermesTopic":topicEnding}
            except Exception as e:
                print("ERROR: mqtt.on_message ERROR nlu: ",e)

        ##################################################################
        ##     INTENT                                                   ##
        ##################################################################
        elif 'hermes/intent/' in topic:
            try:
                dic = {"hermes":HermesComponent.intent.value,"hermesTopic":topicEnding}
            except Exception as e:
                print("ERROR: mqtt.on_message INTENT : ",e)

        ##################################################################
        ##     NLU                                                      ##
        ##################################################################
        elif 'hermes/nlu/' in topic:
            try:
                dic = {"hermes":HermesComponent.nlu.value,"hermesTopic":topicEnding}
            except Exception as e:
                print("ERROR: mqtt.on_message NLU {}: ".format(topicEnding), e)

        ##################################################################
        ##     Dialogue Manager                                         ##
        ##################################################################
        elif 'hermes/dialogueManager/' in topic:
            try:
                dic = {"hermes":HermesComponent.dialogueManager.value,"hermesTopic":topicEnding}
            except Exception as e:
                print("ERROR: mqtt.on_message DialogueManager {}: ".format(topicEnding), e)
        
    
    #convert payload json data into database fields
    intentSlots = []
    if payload:
        if 'siteId' in payload:
            dic['siteId'] = payload['siteId']
        if 'modelId' in payload:
            dic['modelId'] = payload['modelId']
        if 'sessionId' in payload:
            dic['sessionId'] = payload['sessionId']
        if 'reactivatedFromSessionId' in payload:
            dic['reactivatedFromSessionId'] = payload['reactivatedFromSessionId']
        if 'text' in payload:
            dic['text'] = payload['text']
        if 'customData' in payload:
            dic['customData'] = payload['customData']
        if 'input' in payload:
            dic['intentinput'] = payload['input']
        if 'intentFilter' in payload:
            dic['intentFilter'] = payload['intentFilter']
        if 'sendIntentNotRecognized' in payload:
            dic['sendIntentNotRecognized'] = payload['sendIntentNotRecognized']
        
        
        
        if 'init' in payload:
            #startSession has added info inside an inclosed dict
            dic['startsessiontype'] = payload['init']['type'] #not optional
            if 'text' in payload['init']:
                dic['text'] = payload['init']['text']
            if 'canBeEnqueued' in payload['init']:
                dic['canBeEnqueued'] = payload['init']['canBeEnqueued']
            if 'intentFilter' in payload['init']:
                dic['intentFilter'] = payload['init']['intentFilter']
            if 'sendIntentNotRecognized' in payload['init']:
                dic['sendIntentNotRecognized'] = payload['init']['sendIntentNotRecognized']

        
    
        if 'intent' in payload:
            dic['intent'] = payload['intent']['intentName']
            dic['confidenceScore'] = payload['intent']['confidenceScore']
            if 'slots' in payload:
                print("\n\n\n\nSLOTS!!!!\n\n\n\n\n")
                for slotitem in payload['slots']:
                    new_slot = Slots(rawValue=slotitem['rawValue'],
                                    kind=slotitem['value']['kind'],
                                    value=slotitem['value']['value'],
                                    entity=slotitem['entity'],
                                    slotName=slotitem['slotName'],
                                    confidenceScore=slotitem['confidenceScore'])
                    intentSlots.append(new_slot)



        if 'termination' in payload:
            #startEnded has added info inside an inclosed dict
            dic['termination'] = SessionEndedReason[payload['termination']['reason']].value #not optional
            if 'error' in payload['termination']:
                dic['terminationerror'] = payload['termination']['error']

       
    #we check to see if the device is in the device list
    #if its a new device that is unknown to the database 
    #we add it
    global devices
    if 'siteId' in dic:
        if not dic['siteId'] in devices:
            new_site = Site(name=dic['siteId'])
            db.session.add(new_site)
            db.session.flush()
            #reload list to get new item ID
            loadSiteDictionary()

        #set the siteId to the INTEGER id field in the db
        dic['siteId'] = devices[dic['siteId']]


    logEntry = Mqttlog(**dic) #create new db row record
   
    #db.session.flush()
    if len(intentSlots) > 0:
        for s in intentSlots:
            logEntry.slots_id.append(s)
            #s.mqttlogId = logEntry.id
            #db.session.add(s)
    
    # commit data
    db.session.add(logEntry) # add new record
    db.session.commit() #save database

    