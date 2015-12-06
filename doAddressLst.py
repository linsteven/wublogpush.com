#coding=utf-8
import requests, json
import os
from log import LogSubscribe, LogUnsubscribe

addUrl = "http://sendcloud.sohu.com/webapi/list_member.add.json"
delUrl = "http://sendcloud.sohu.com/webapi/list_member.delete.json"

API_USER = 'linsteven_wu_confirm'
API_KEY = os.environ.get('API_KEY')
subscribe_list_addr = "wublogpush@maillist.sendcloud.org"
unsubscribe_list_addr = "unsubscribe@maillist.sendcloud.org"

def addToAddrLst(email):
    addr = email
    params = {
      "api_user": API_USER,
      "api_key" : API_KEY,
      "mail_list_addr" : subscribe_list_addr,
      "member_addr" : addr,
      "upsert" : "true",
      }
    r = requests.post(addUrl, files={}, data=params)
    LogSubscribe(email + " list_member.add " + r.text)

def delFromAddrLst(email):
    addr = email
    params = {
      "api_user": API_USER,
      "api_key" : API_KEY,
      "mail_list_addr" : subscribe_list_addr,
      "member_addr" : addr,
      }
    r = requests.post(delUrl, files={}, data=params)
    LogUnsubscribe(email + " list_member.delete " + r.text)
    #unsubscribes.add
    params = {
      "api_user": API_USER,
      "api_key" : API_KEY,
      "mail_list_addr" : unsubscribe_list_addr,
      "member_addr" : addr,
      "upsert" : "true",
      }
    r = requests.post(addUrl, files={}, data=params)
    line = '\n-----------------\n'
    LogUnsubscribe(email + " unsubscribes.add " + r.text + line)

#addToAddrLst("763061206@qq.com")
#addToAddrLst("1656758436@qq.com")
#delFromAddrLst("12345678@qq.com")
