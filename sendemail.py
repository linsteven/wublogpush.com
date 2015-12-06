#coding=utf-8
import requests, json
import time
import os
from log import LogEmailActivate, LogEmailSuccess, LogEmailUnsubscribe
from doAddressLst import delFromAddrLst

mailUrl = "http://sendcloud.sohu.com/webapi/mail.send_template.json"

API_USER = 'linsteven_wu_confirm'
API_KEY = os.environ.get('API_KEY')

def sendActivate(email, token) :
  toLst = list()
  tokenLst = list()
  toLst.append(email)
  tokenLst.append(token)
  sub_vars = {
    'to': toLst,
    'sub':{
      '%token%': tokenLst,
      '%email%': toLst,
      }
    }
  params = {
    "api_user": API_USER,
    "api_key" : API_KEY,
    "template_invoke_name" : "template_activate",
    "substitution_vars" : json.dumps(sub_vars),
    "from" : "wu@batch.wublogpush.com",
    "fromname" : "吴姐推送",
    "subject" : "欢迎订阅吴姐推送，请尽快完成激活！",
    "resp_email_id": "true",
    }
  r = requests.post(mailUrl, files={}, data=params)
  LogEmailActivate(email + ' ' + token + ' ' + r.text)

def sendSuccess(email) :
  toLst = list()
  toLst.append(email)
  sub_vars = {
    'to': toLst,
    'sub':{
      '%email%': toLst,
      }
    }
  params = {
    "api_user": API_USER,
    "api_key" : API_KEY,
    "template_invoke_name" : "template_success",
    "substitution_vars" : json.dumps(sub_vars),
    "from" : "wu@batch.wublogpush.com",
    "fromname" : "吴姐推送",
    "subject" : "恭喜您成功订阅吴姐推送！",
    "resp_email_id": "true",
    }
  r = requests.post(mailUrl, files={}, data=params)
  LogEmailSuccess(email + ' ' + r.text)

def sendUnsubscribe(email, token):
  toLst = list()
  toLst.append(email)
  tokenLst = list()
  tokenLst.append(token)
  sub_vars = {
    'to': toLst,
    'sub':{
      '%token%': tokenLst,
      }
    }
  params = {
    "api_user": API_USER,
    "api_key" : API_KEY,
    "template_invoke_name" : "template_unsubscribe",
    "substitution_vars" : json.dumps(sub_vars),
    "from" : "wu@batch.wublogpush.com",
    "fromname" : "吴姐推送",
    "subject" : "感谢你对吴姐推送的一路支持！",
    "resp_email_id": "true",
    }
  r = requests.post(mailUrl, files={}, data=params)
  LogEmailUnsubscribe(email + ' ' + r.text)

#sendActivate('1656758436@qq.com','esfhweufbwefnweifw')
#sendSuccess('1656758436@qq.com')
#sendUnsubscribe('1656758436@qq.com', 'fsagergreher')
