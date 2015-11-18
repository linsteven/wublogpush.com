#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template,redirect, url_for
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Email
from flaskext.markdown import Markdown
from flask import Markup
from flask.ext.sqlalchemy import SQLAlchemy

basedir = "/home/yyl/WuBlogPush2"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + os.path.join(basedir, 'wuPushes.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
Markdown(app)
app.secret_key = os.environ.get('SECKET_KEY') or \
    ' \x9c6-\xe9\xbb\xd0\xea\xf8F\xde\xb5wy\x99,G\xbd\xe8\xe8\xb3_\x08!'

class Push(db.Model):
    __tablename__ = 'Pushes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    time = db.Column(db.Text)
    news = db.Column(db.Text)
    deals = db.Column(db.Text)
    content = db.Column(db.Text)

    def __repr__(self):
        return '<Mesg %r>' % self.content

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
        # send email of validation
        form.email.data = ''
    return render_template('index.html',form=form)

@app.route('/pushes/<int:push_id>', methods=['GET'])
def pushes(push_id):
    push = Push.query.filter_by(id=push_id).first()
    if push is None:
        return render_template('pushes.html')
    else:
        return render_template('pushes.html', 
            pushTitle = push.title, pushTime = push.time,
            news = push.news, deals = push.deals, 
            content = push.content)

@app.route('/pushes/', methods=['GET'])
def latestPush():
    latestPushId = Push.query.order_by('-id').first().id
    print latestPushId
    return redirect(url_for('pushes', push_id=latestPushId))
    #    return render_template('pushes.html', 
    #        pushTitle = push.title, pushTime = push.time,
    #        news = push.news, deals = push.deals, 
    #        content = push.content)

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

if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True)
