#coding=utf-8
import time
import datetime

def LogEmailActivate(mesg) :
  dt = datetime.datetime.now()
  date = dt.strftime('%Y%m')
  logFile = open('./Log/emailActivate_' + date + '.log','a')
  ctime = dt.strftime('%m-%d %H:%M:%S  ')
  logFile.write(ctime + mesg + '\n')
  logFile.close()

def LogEmailSuccess(mesg):
  dt = datetime.datetime.now()
  date = dt.strftime('%Y%m')
  logFile = open('./Log/emailSuccess_' + date + '.log','a')
  ctime = dt.strftime('%m-%d %H:%M:%S  ')
  logFile.write(ctime + mesg  + '\n')
  logFile.close()
    
def LogAddToAddr(mesg):
  dt = datetime.datetime.now()
  date = dt.strftime('%Y%m')
  logFile = open('./Log/addToAddr_' + date + '.log','a')
  ctime = dt.strftime('%m-%d %H:%M:%S  ')
  logFile.write(ctime + mesg  + '\n')
  logFile.close()
