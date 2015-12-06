#coding=utf-8
import time
import datetime

def LogEmailActivate(mesg) :
  dt = datetime.datetime.now()
  date = dt.strftime('%Y%m')
  logFile = open('./Log/emailActivate_' + date + '.log','a')
  ctime = dt.strftime('%m-%d %H:%M:%S  ')
  logFile.write(ctime + mesg + '\n\n')
  logFile.close()

def LogEmailSuccess(mesg):
  dt = datetime.datetime.now()
  date = dt.strftime('%Y%m')
  logFile = open('./Log/emailSuccess_' + date + '.log','a')
  ctime = dt.strftime('%m-%d %H:%M:%S  ')
  logFile.write(ctime + mesg  + '\n\n')
  logFile.close()
    
def LogEmailUnsubscribe(mesg):
  dt = datetime.datetime.now()
  date = dt.strftime('%Y%m')
  logFile = open('./Log/emailUnsubscribe_' + date + '.log','a')
  ctime = dt.strftime('%m-%d %H:%M:%S  ')
  logFile.write(ctime + mesg  + '\n\n')
  logFile.close()

def LogSubscribe(mesg):
  dt = datetime.datetime.now()
  date = dt.strftime('%Y%m')
  logFile = open('./Log/subscribe_' + date + '.log','a')
  ctime = dt.strftime('%m-%d %H:%M:%S  ')
  logFile.write(ctime + mesg  + '\n\n')
  logFile.close()

def LogUnsubscribe(mesg):
  dt = datetime.datetime.now()
  date = dt.strftime('%Y%m')
  logFile = open('./Log/unsubscribe_' + date + '.log','a')
  ctime = dt.strftime('%m-%d %H:%M:%S  ')
  logFile.write(ctime + mesg  + '\n\n')
  logFile.close()


def LogDebug(mesg):
  dt = datetime.datetime.now()
  date = dt.strftime('%Y%m')
  logFile = open('./Log/debug_' + date + '.log','a')
  ctime = dt.strftime('%m-%d %H:%M:%S  ')
  logFile.write(ctime + mesg  + '\n\n')
  logFile.close()
