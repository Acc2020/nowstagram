# -*- encoding = UTF-8 -*-

from nowstagram import db
from datetime import datetime
import random


class Image(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True )
    url = db.Column(db.String(512))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_id = db.Column(db.DateTime)

    def __init__(self, user_id, url):
        self.url = url
        self.user_id = user_id
        self.created_id = datetime.now()

    def __repr__(self):
        return '<Image %d %s>' % (self.id, self.url)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(32))
    head_url = db.Column(db.String(256))
    images = db.relationship('Image')

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.head_url = 'http://images.nowscoder.com/head/' + str(random.randint(0,1000))+'m.png'

    def __repr__(self):
        return '<User %d %s> ' % (self.id, self.username)