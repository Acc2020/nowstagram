# -*- encoding = UTF-8 -*-

from nowstagram import app
from nowstagram.models import User, Image
from flask import render_template, redirect, request, flash


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

@app.route('/reg/')
def reg():
    # request.args requser.form
    username = request.values.get('username').strip()
    password = request.values.get('username').strip()

    user = User.query.filter_by(username=username).first()
    if user != None:
        redirect_with_msg(u'用户名已经存在','relogin')
        return redirect('/regloginpage/')
