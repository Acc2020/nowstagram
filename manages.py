# -*- encoding = UTF-8 -*-

from nowstagram import app,db
from flask_script import Manager
from nowstagram.models import  User, Image, Comment
import random
manager = Manager(app)

def get_image_url():
    return 'http://images.nowscoder.com/head/' + str(random.randint(0,1000))+'m.png'

@manager.command
def init_database():
    db.drop_all()
    db.create_all()
    for i in range(0,100):
        db.session.add(User('User' + str(i),'a'+str(i)))
        for j in range (0,3):
            db.session.add(Image(get_image_url(), i+1))
            for k in range (0,3):
                db.session.add(Comment('This is comment' + str(k),  1+i*3 +j, i+1 ))
    db.session.commit()

if __name__ == '__main__':
    manager.run()
