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
    #mqttlog_id = Column(ForeignKey('mqttlog.id'), primary_key=True)
    #mqttlog_id = relationship("Mqttlog")
    #mqttlog = relationship("Mqttlog")
    #mqttlogs_ids = relationship("MQTTLog", primaryjoin="Site.id==MQTTLog.site_id")

    def __repr__(self):
        return '{}'.format(self.name) 

    @hybrid_property
    def fullsitename(self):
        return self.site.name

