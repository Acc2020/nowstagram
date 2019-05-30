#-*- encoding = UTF-8 -*-

from nowstagram import app,db
from nowstagram.models import User, Image
from flask import render_template, redirect, request, flash
import random ,hashlib

@app.route('/')
def index():
    images = Image.query.order_by((Image.id.desc())).limit(10).all()
    return render_template('index.html', images=images)


@app.route('/image/<int:image_id>/')
def image(image_id):
    image = Image.query.get(image_id)
    if image == None:
        return redirect('/')
    return render_template('pageDetail.html', image=image)


@app.route('/profile/<int:user_id>/')
def profile(user_id):
    user = User.query.get(user_id)
    if user == None:
        return redirect('/')
    return render_template('profile.html', user=user)


@app.route('/regloginpage/')
def regloginpage():

    return render_template('login.html')


def redirect_with_msg(target, msg, category):
    if msg != None:
        flash(msg,category=category)
    return redirect(target)

@app.route('/reg/',methods={'post','get'})
def reg():
    # request.args requser.form
    username = request.values.get('username').strip()
    password = request.values.get('username').strip()

    if (username == ''or password == ''):
        redirect_with_msg('/regloginpage/', u'用户名或密码不能为空','relogin')

    user = User.query.filter_by(username=username).first()
    if user != None:
        redirect_with_msg('/regloginpage/',u'用户名已经存在','relogin')

    salt = '.'.join(random.sample('0123456789abcdefghigkABCDEFGHIGK',10))
    m = hashlib.md5()
    m.update(password.encode("utf-8")+salt.encode("utf-8"))
    password = m.hexdigest()
    user = User(username, password, salt)
    db.session.add(user)
    db.session.commit()

    return redirect('/')


