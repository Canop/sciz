#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
import random, string, hashlib, base64, os
from sqlalchemy import Column, Integer, String, DateTime, event
from sqlalchemy.orm import relationship
import modules.globals as sg

# Class of a Notification
class GROUP(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    flat_name = Column(String(50), unique=True)
    name = Column(String(50), unique=True)
    desc = Column(String(255))
    blason_url = Column(String(255))
    mail = Column(String(150))
    mail_pwd = Column(String(255))
    
    # Associations Many-To-Many
    users = relationship('AssocUsersGroups', back_populates='group')
    # Associations Many-To-One
    confs = relationship('CONF', back_populates='group')
    trolls = relationship('TROLL', back_populates='group')
    mobs = relationship('MOB', back_populates='group')
    hooks = relationship('HOOK', back_populates='group')
    events = relationship('EVENT', back_populates='group')
    battles = relationship('BATTLE', back_populates='group')
    cdms = relationship('CDM', back_populates='group')
    pieges = relationship('PIEGE', back_populates='group')

    # Constructor is handled by SqlAlchemy, do not override

@event.listens_for(GROUP, 'before_insert')
def generate_random_pwd_hash(mapper, connection, target):
    # Generate a random long whatever
    # (mail_pwd is used for maintaining postfix-accounts.cf but accounts should not be used by end-users)
    pwd = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(42))
    # Hash
    salt = os.urandom(64) # Creates a random 64 byte string
    shahash = hashlib.sha512()
    shahash.update(pwd)
    shahash.update(salt)
    shahashsalt = '{}{}'.format(shahash.digest(), salt)
    pwd_hash = base64.b64encode(shahashsalt)
    target.mail_pwd = "{SSHA512}%s" % (pwd_hash)
