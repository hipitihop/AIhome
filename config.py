#!/usr/bin/env python3
# -*- coding:utf-8 -*-

### **************************************************************************** ###
### Only change these setting for your setup
### **************************************************************************** ###

# Port to run site on
PORT = 80

#Theme 
# 1 - dark theme
# 2 - light theme
THEME = 1

#Theme colour scheme
# 1 - green
# 2 - blue
# 3 - red
# 4 - purple
THEME_COLOUR = 2


# MQTT
MQTT_BROKER_URL = 'localhost'  # broker url
MQTT_BROKER_PORT = 1883  # default port for non-tls connection
MQTT_USERNAME = ''  # set the username here if you need authentication for the broker
MQTT_PASSWORD = ''  # set the password here if the broker demands authentication
MQTT_KEEPALIVE = 60  # set the time interval for sending a ping to the broker to 5 seconds
MQTT_TLS_ENABLED = False  














### **************************************************************************** ###
### Only change these setting for you know what your doing !!!!!!!!!!!!!!!!!!
### You have been warned :)
### **************************************************************************** ###


TESTING = False
FLASK_ENV = 'production' #'development'
FLASK_DEBUG = False
DEVELOPMENT = False
DEBUG = False

# Create dummy secrey key so we can use sessions
SECRET_KEY = 'iuechtqpthcq98'

# Create in-memory database
DATABASE_FILE = 'db.sqlite'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_FILE
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-Security config
SECURITY_URL_PREFIX = "/"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "sdfbcasdjhJBHJDw9w24JKBwejrw"
SECURITY_LOGIN_URL = "/login"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_UNAUTHORIZED_VIEW = "/"
SECURITY_POST_CHANGE_VIEW = "/"
SECURITY_POST_LOGIN_VIEW = "/"
SECURITY_POST_LOGOUT_VIEW = "/"
SECURITY_POST_REGISTER_VIEW = "/"
SECURITY_POST_RESET_VIEW = "/"
SECURITY_REGISTERABLE = False
SECURITY_RECOVERABLE = False
SECURITY_CHANGEABLE = True
SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False
SECURITY_FLASH_MESSAGES = False

