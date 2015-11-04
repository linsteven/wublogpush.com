#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Email
from flaskext.markdown import Markdown
from flask import Markup

app = Flask(__name__)
bootstrap = Bootstrap(app)
Markdown(app)
app.secret_key = os.environ.get('SECKET_KEY') or \
    ' \x9c6-\xe9\xbb\xd0\xea\xf8F\xde\xb5wy\x99,G\xbd\xe8\xe8\xb3_\x08!'

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


if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True)
