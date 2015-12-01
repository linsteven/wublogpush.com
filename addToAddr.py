#coding=utf-8
import requests, json
import os
from log import LogAddToAddr

addUrl = "http://sendcloud.sohu.com/webapi/list_member.add.json"

API_USER = 'trigger_wu_test'
API_KEY = os.environ.get('API_KEY')

def addToAddrLst(email):
    myvars = '''{"id":"","title":"","news":"","deals":"",\
            "content":"","url":""}'''
    addr = email
    params = {
      "api_user": API_USER,
      "api_key" : API_KEY,
      "mail_list_addr" : "justfortest@maillist.sendcloud.org",
      "member_addr" : addr,
      "vars" : myvars,
      "upsert" : "true",
      }
    r = requests.post(addUrl, files={}, data=params)
    LogAddToAddr(email + " " + r.text)

