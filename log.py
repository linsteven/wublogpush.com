#coding=utf-8
import sys
import time

def LogError(mesg) :
  date = time.strftime('%Y%m%d',time.localtime(time.time()))
  logFile = open('error_' + date + '.log', 'a')
  logFile.write(mesg + '\n')
  logFile.close()

