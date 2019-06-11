# -*- encoding = UTF-8 -*-

from nowstagram import app, db, login_manager
from nowstagram.models import User, Image, Comment
from flask import render_template, redirect, request, flash, get_flashed_messages, send_from_directory, Flask
import random, hashlib, json, uuid, os
from flask_login import login_user, logout_user, current_user, login_required
from qiniusdk import qiniu_upload_file


@app.route('/index/images/<int:page>/<int:per_page>/')
def index_images(page, per_page):
    paginate = Image.query.order_by(db.desc(Image.id)).paginate(page=page, per_page=per_page, error_out=False)
    map = {'has_next': paginate.has_next}
    images = []
    for image in paginate.items:
        comments = []
        for i in range(0, min(2, len(image.comments))):
            comment = image.comments[i]
            comments.append({'username':comment.user.username,
                             'user_id':comment.user_id,
                             'content':comment.content})
        imgvo = {'id': image.id,
                 'url': image.url,
                 'comment_count': len(image.comments),
                 'user_id': image.user_id,
                 'head_url':image.user.head_url,
                 'created_date':str(image.created_date),
                 'comments':comments}
        images.append(imgvo)

    map['images'] = images
    return json.dumps(map)



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
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    if user == None:
        return redirect('/')
    paginate = Image.query.paginate(page=1, per_page=3)
    return render_template('profile.html', user=user, has_next=paginate.has_next, images=paginate.items)


@app.route('/profile/images/<int:user_id>/<int:page>/<int:per_page>/')
def user_images(user_id, page, per_page):
    # 参数检查
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page)
    map = {'has_next': paginate.has_next}
    images = []
    for image in paginate.items:
        imgvo = {'id': image.id, 'url': image.url, 'comment_count': len(image.comments)}
        images.append(imgvo)
    map['images'] = images
    return json.dumps(map)


@app.route('/regloginpage/')
def regloginpage():
    msg = ''
    for m in get_flashed_messages(with_categories=False, category_filter=['relogin']):
        msg = msg + m
    return render_template('login.html', msg=msg)


def redirect_with_msg(target, msg, category):
    if msg != None:
        flash(msg, category=category)
    return redirect(target)


@app.route('/login/', methods={'post', 'get'})
def login():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()

    user = User.query.filter_by(username=username).first()

    if (username == '' or password == ''):
        return redirect_with_msg('/regloginpage', u'用户名或密码不能为空', 'relogin')

    if (user == None):
        return redirect_with_msg('/regloginpage', u'用户名不存在', 'relogin')

    m = hashlib.md5()
    m.update(password.encode('utf-8') + user.salt.encode('utf-8'))
    if (m.hexdigest() != user.password):
        return redirect_with_msg('/reglogin', u'密码不正确', 'relogin')

    login_user(user)

    return redirect('/')


@app.route('/reg/', methods={'post', 'get'})
def reg():
    # request.args requser.form
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()

    user = User.query.filter_by(username=username).first()
    if (username == '' or password == ''):
        return redirect_with_msg('/regloginpage', u'用户名或密码不能为空', 'relogin')
    if user != None:
        return redirect_with_msg('/regloginpage', u'用户名已经存在', 'relogin')
    salt = '.'.join(random.sample('0123456789abcdefghigkABCDEFGHIGK', 10))
    m = hashlib.md5()
    m.update(password.encode("utf-8") + salt.encode("utf-8"))
    password = m.hexdigest()
    user = User(username, password, salt)
    db.session.add(user)
    db.session.commit()

    login_user(user)

    return redirect('/')


@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/')


@app.route('/image/<image_name>')
def view_image(image_name):
    return send_from_directory(app.config['UPLOAD_DIR'], image_name)


@app.route('/addcomment/', methods={'post'})
@login_required
def add_comment():
    image_id = int(request.values['image_id'])
    content = request.values['content']
    comment = Comment(content, image_id, current_user.id)
    db.session.add(comment)
    db.session.commit()
    return json.dumps({"code":0, "id":comment.id,
                       "content":comment.content,
                       "username":comment.user.username,
                       "user_id":comment.user_id})

def save_to_qiniu(file, file_name):
    return qiniu_upload_file(file, file_name)

def save_to_local(file, file_name):
    save_dir = app.config['UPLOAD_DIR']
    file.save(os.path.join(save_dir, file_name))
    return '/image/' + file_name

@app.route('/upload/', methods={"post"})
@login_required
def upload():
    file = request.files['file']
    # http://werkzeug.pocoo.org/docs/0.10/datastructures/
    # 需要对文件进行裁剪等操作
    file_ext = ''
    if file.filename.find('.') > 0:
        file_ext = file.filename.rsplit('.', 1)[1].strip().lower()
    if file_ext in app.config['ALLOWED_EXT']:
        file_name = str(uuid.uuid1()).replace('-', '') + '.' + file_ext
        url = qiniu_upload_file(file, file_name)
        #url = save_to_local(file, file_name)
        if url != None:
            db.session.add(Image(url, current_user.id))
            db.session.commit()

    return redirect('/profile/%d' % current_user.id)

#11111
