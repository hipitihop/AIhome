from flask_sqlalchemy import SQLAlchemy
import logging

db = SQLAlchemy()


#flask db init
#flask db migrate
#flask db upgrade
#
#


from models.admin import Role, User
from models.site import Site
from models.mqttlog import Mqttlog, SessionEndedReason, HermesComponent
from models.slots import Slots