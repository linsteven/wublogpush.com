#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import datetime
from flask import Flask, render_template,redirect, url_for, flash
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

#basedir = "/home/yyl/WuBlogPush2"
basedir = "/Users/yyl/Projects/WuBlogPush2"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + os.path.join(basedir, 'wublogpush.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
Markdown(app)
app.secret_key = os.environ.get('SECR_KEY') or \
    ' \x9c6-\xe9\xbb\xd0\xea\xf8F\xde\xb5wy\x99,G\xbd\xe8\xe8\xb3_\x08!'

class Push(db.Model):
    __tablename__ = 'pushes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    time = db.Column(db.Text)
    news = db.Column(db.Text)
    deals = db.Column(db.Text)
    content = db.Column(db.Text)
    url = db.Column(db.Text)

    def __repr__(self):
        return '<Mesg %r>' % self.content

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


@app.route('/', methods=['GET', 'POST'])
def index():
    email = None
    form = EmailForm()
    if form.validate_on_submit():
        email = form.email.data
        email = str(email)
        isConfirmed = False
        #add user to db
        user = User.query.filter_by(email=email).first()
        token = generate_confirmation_token(email)
        if user is None:
            user = User(email=email,token=token,confirmed=False)
            db.session.add(user)
            db.session.commit()
        elif user.confirmed:
            isConfirmed = True
            flash(u'您已订阅过吴姐推送。<br>\
                    如果您还没有收到过任何吴姐推送的邮件，\
                    请<a href="http://wublogpush.com/about/"><b>联系我</b></a>')
        else:
            user.subscribed_on = datetime.datetime.now()
            db.session.add(user)
            db.session.commit()
        # send email of validation
        if isConfirmed is False:
            sendActivate(email, token)
            flash(u'您已成功订阅吴姐推送，请尽快进入您的邮箱 ' + email + u' 完成激活。')
        form.email.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',form=form)

@app.route('/activate/<string:token>', methods=['GET'])
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash(u'链接无效，请重新订阅！')
    if email is False:
        flash(u'链接无效，请重新订阅！')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed is False:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        user.unsubscribed = False
        db.session.add(user)
        db.session.commit()
        sendSuccess(email)
        addToAddrLst(email)
    flash(email + u' 您已成功订阅吴姐推送！')
    return redirect(url_for('index'))

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

@app.route('/pushes/<int:push_id>', methods=['GET'])
def pushes(push_id):
    push = Push.query.filter_by(id=push_id).first_or_404()
    return render_template('pushes.html', 
        pushTitle = push.title, pushTime = push.time,
        news = push.news, deals = push.deals, 
        content = push.content, url = push.url)

@app.route('/pushes/', methods=['GET'])
def latestPush():
    latestPushId = Push.query.order_by('-id').first_or_404().id
    return redirect(url_for('pushes', push_id=latestPushId))

@app.route('/FAQ/', methods=['GET'])
def FAQ():
    return render_template('FAQ.html')

@app.route('/donate/', methods=['GET'])
def donate():
    return render_template('donate.html')

@app.route('/about/', methods=['GET'])
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
    app.run(host="127.0.0.1", debug=True)
