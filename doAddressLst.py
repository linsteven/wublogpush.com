#coding=utf-8
import requests, json
import os
from log import LogAddToAddr, LogDelFromAddr

addUrl = "http://sendcloud.sohu.com/webapi/list_member.add.json"
delUrl = "http://sendcloud.sohu.com/webapi/list_member.delete.json"
addUnsubcribeUrl = "http://sendcloud.sohu.com/webapi/unsubscribes.add.json"
delUnsubcribeUrl = "http://sendcloud.sohu.com/webapi/unsubscribes.delete.json"

API_USER = 'trigger_wu_test'
API_KEY = os.environ.get('API_KEY')
mail_list_addr = "justfortest@maillist.sendcloud.org"

def addToAddrLst(email):
    myvars = '''{"id":"","title":"","news":"","deals":"",\
            "content":"","url":"","user_defined_unsubscribe_link":""}'''
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
    params = {
      "api_user": API_USER,
      "api_key" : API_KEY,
      "email" : addr,
      }
    r = requests.post(delUnsubcribeUrl, files={}, data=params)

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

#addToAddrLst("763061206@qq.com")
#addToAddrLst("1656758436@qq.com")
#delFromAddrLst("12345678@qq.com")
