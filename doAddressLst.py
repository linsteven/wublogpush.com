#coding=utf-8
import requests, json
import os
from log import LogAddToAddr, LogDelFromAddr

addUrl = "http://sendcloud.sohu.com/webapi/list_member.add.json"
delUrl = "http://sendcloud.sohu.com/webapi/list_member.delete.json"
addUnsubcribeUrl = "http://sendcloud.sohu.com/webapi/unsubscribes.add.json"

API_USER = 'trigger_wu_test'
API_KEY = os.environ.get('API_KEY')
mail_list_addr = "justfortest@maillist.sendcloud.org"

def addToAddrLst(email):
    myvars = '''{"id":"","title":"","news":"","deals":"",\
            "content":"","url":""}'''
    addr = email
    params = {
      "api_user": API_USER,
      "api_key" : API_KEY,
      "mail_list_addr" : mail_list_addr,
      "member_addr" : addr,
      "vars" : myvars,
      "upsert" : "true",
      }
    r = requests.post(addUrl, files={}, data=params)
    LogAddToAddr(email + " " + r.text)

def delFromAddrLst(email):
    addr = email
    params = {
      "api_user": API_USER,
      "api_key" : API_KEY,
      "mail_list_addr" : mail_list_addr,
      "member_addr" : addr,
      }
    r = requests.post(delUrl, files={}, data=params)
    LogDelFromAddr(email + " " + r.text)
    #unsubscribes.add
    params = {
      "api_user": API_USER,
      "api_key" : API_KEY,
      "email" : addr,
      }
    r = requests.post(addUnsubcribeUrl, files={}, data=params)
    LogDelFromAddr(email + " unsubscribes.add " + r.text)

#addToAddrLst("12345678@qq.com")
#delFromAddrLst("12345678@qq.com")
