#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
import datetime
from flask import Flask, render_template,redirect, url_for, flash
from flask import request
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Email
from flaskext.markdown import Markdown
from flask import Markup
from flask.ext.sqlalchemy import SQLAlchemy
from mytoken import generate_confirmation_token, confirm_token
from sendemail import sendActivate, sendSuccess, sendUnsubscribe
from doAddressLst import addToAddrLst, delFromAddrLst

reload(sys)
sys.setdefaultencoding('utf8')
#basedir = "/home/yyl/WuBlogPush2"
basedir = "/Users/yyl/Projects/WuBlogPush2"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + os.path.join(basedir, 'wublogpush.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = os.environ.get('SECR_KEY') or \
    ' \x9c6-\xe9\xbb\xd0\xea\xf8F\xde\xb5wy\x99,G\xbd\xe8\xe8\xb3_\x08!'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
Markdown(app)

class Push(db.Model):
    __tablename__ = 'pushes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    time = db.Column(db.Text)
    deals = db.Column(db.Text)
    changes = db.Column(db.Text)
    content = db.Column(db.Text)
    url = db.Column(db.Text)
    news = db.Column(db.Text)

    def __repr__(self):
        return '<Mesg %r>' % self.content

class Position(db.Model):
    __tablename__ = 'positions'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Text)
    size = db.Column(db.Text)
    content = db.Column(db.Text)
    deals = db.Column(db.Text)
    push_id = db.Column(db.Text)

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Mesg %r>' % self.id

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    token = db.Column(db.Text, unique=True, nullable=False)
    subscribed_on = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    unsubscribed = db.Column(db.Boolean, nullable=False, default=False)
    unsubscribed_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, email, token, confirmed):
        self.email = email
        self.token = token
        self.subscribed_on = datetime.datetime.now()
        self.confirmed = confirmed
        self.confirmed_on = None
        self.unsubscribed = False
        self.unsubscribed_on = None

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<email {}'.format(self.email)


class EmailForm(Form):
    email = StringField(u"电子邮箱",[InputRequired(u"请输入邮箱"),\
          Email(u"请输入正确的邮箱")])
    submit = SubmitField(u'立即订阅')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email']
    if not re.match(r'^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$', email):
        return "请输入正确的邮箱"
    isConfirmed = False
    #add user to db
    try:
        user = User.query.filter_by(email=email).first()
    except:
        user = None
    token = generate_confirmation_token(email)
    if user is None:
        user = User(email=email,token=token,confirmed=False)
        db.session.add(user)
        db.session.commit()
    elif user.confirmed and user.unsubscribed is False:
        isConfirmed = True
        return '''您已订阅过小王子推送。如果您还没有收到过任何小王子推送的邮件,请联系我们'''
    else:
        user.subscribed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
    # send email of validation
    if isConfirmed is False:
        sendActivate(email, token)
        return '请尽快进入您的邮箱<' + email + '>完成激活，激活后即可订阅成功！'


@app.route('/activate/<string:token>', methods=['GET'])
def confirm_email(token):
    mesg = ''
    try:
        email = confirm_token(token)
    except:
        mesg = u'链接无效，请重新订阅！'
    if email is False:
        mesg = u'链接无效，请重新订阅！'
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed is False:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        addToAddrLst(email)
        sendSuccess(email)
    elif user.confirmed is True  and user.unsubscribed is True:
        user.unsubscribed = False
        db.session.add(user)
        db.session.commit()
        addToAddrLst(email)
        sendSuccess(email)
    if not mesg:
        mesg = email + u' 恭喜您成功订阅小王子推送！'
    return render_template('activate.html', message = mesg)

@app.route('/unsubscribe/<string:token>', methods=['GET'])
def unsubscribe(token):
    try:
        email = confirm_token(token)
    except:
        flash(u'链接无效！')
    user = User.query.filter_by(email=email).first_or_404()
    if user.unsubscribed is False:
        user.unsubscribed = True
        user.unsubscribed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        sendUnsubscribe(email, token)
        delFromAddrLst(email)
    return render_template('unsubscribe.html')

@app.route('/pushes/<int:push_id>', methods=['GET'])
def pushes(push_id):
    MAXID = 365 * 10 * 100
    lastest_id = Push.query.order_by('-id').first_or_404().id
    if push_id == 0:
        flash(u'已是最早一篇')
        return redirect(url_for('pushes', push_id=1))
    elif push_id == MAXID :
        flash(u'已是最新一篇')
        return redirect(url_for('pushes', push_id=lastest_id))
    else:
        pre_id = push_id - 1
        next_id = push_id + 1
        if push_id == lastest_id:
            next_id = MAXID
        cur_id = push_id
    push = Push.query.filter_by(id=cur_id).first_or_404()
    return render_template('pushes.html',
        pushId = push_id, preId = pre_id, nextId = next_id,
        pushTitle = push.title, pushTime = push.time,
        news = push.news, deals = push.deals,changes=push.changes,
        content = push.content, url = push.url)

@app.route('/pushes', methods=['GET'])
def latestPush():
    try:
        latestPushId = Push.query.order_by('-id').first_or_404().id
    except:
        return render_template('404.html'), 404
    return redirect(url_for('pushes', push_id=latestPushId))

@app.route('/positions', methods=['GET'])
def positions():
    try:
        latestPosId = Position.query.order_by('-id').first_or_404().id
    except:
        return render_template('404.html'), 404
    #return str(latestPosId)
    my_lst = range(latestPosId - 6, latestPosId + 1)
    positions = Position.query.filter(Position.id.in_(my_lst)).all()
    return render_template('positions.html', positions=positions, size=7)

@app.route('/positions/<int:count>', methods=['GET'])
def positions_count(count):
    try:
        latestPosId = Position.query.order_by('-id').first_or_404().id
    except:
        return render_template('404.html'), 404
    start_id = latestPosId - count + 1
    if start_id < 0:
        start_id = 0
        flash(u"已显示所有仓位信息")
    my_lst = range(start_id, latestPosId + 1)
    positions = Position.query.filter(Position.id.in_(my_lst)).all()
    return render_template('positions.html', positions=positions,size=len(my_lst))

@app.route('/positions/all/<int:count>', methods=['GET'])
def positions_count_all(count):
    try:
        latestPosId = Position.query.order_by('-id').first_or_404().id
    except:
        return render_template('404.html'), 404
    start_id = latestPosId - count + 1
    if start_id < 0:
        start_id = 0
        flash(u"已显示所有仓位信息")
    my_lst = range(start_id, latestPosId + 1)
    positions = Position.query.filter(Position.id.in_(my_lst)).all()
    return render_template('positions.html',
            positions=positions,size=len(my_lst),is_all='all/')

@app.route('/FAQ', methods=['GET'])
def FAQ():
    return render_template('FAQ.html')

@app.route('/thanks', methods=['GET'])
def thanks():
    return render_template('thanks.html')

@app.route('/lastestId')
def api_lastestId():
    latestPushId = Push.query.order_by('-id').first_or_404().id
    return str(latestPushId)

@app.route('/donate', methods=['GET'])
def donate():
    return render_template('donate.html')

@app.route('/activate', methods=['GET'])
def act():
    return render_template('activate.html')

@app.route('/tip', methods=['GET'])
def tip():
    return render_template('tip.html')

@app.route('/about', methods=['GET'])
def about():
    #return url_for('about')
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
  return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
