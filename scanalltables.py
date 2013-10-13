#!/usr/bin/python

import time
scriptstart =  time.time()
import csv

import brybus
import bryqueue
import bryfunc
ByteToHex = bryfunc.ByteToHex
HexToByte = bryfunc.HexToByte

def scantable():
  #load data from csv
  print "Loading table information"
  
  #load CSV into memory
  registers = []
  tfin = csv.reader(open('myregisters.csv', 'rb'))
  for row in tfin:
    registers.append(row)
  
  scan_q = bryqueue.writequeue()
  
  print "Building Queue"
  for r in registers:
    reg = '00' + r[1] + r[6]
    f = brybus.frame(reg,'C',r[0],'3001','0B')
    scan_q.pushframe(f)
          
  return scan_q  

#=======main========

q = scantable()
q.printqueue()

#setup the stream and bus
s = brybus.stream('S','/dev/ttyUSB0')
b = brybus.bus(s)

while(1):
  #write
  wf_raw = q.writeframe()
  wf = brybus.frame(wf_raw,"B")
  w = b.write(wf_raw)
  
  f = brybus.frame(b.read(),"B")
  if w==1:
    print "write", q.printstatus()
    print wf.dst,wf.src,wf.len,wf.func,wf.data,wf.crc
    print f.dst,f.src,f.len,f.func,f.data,f.crc
  q.checkframe(f)
  
  #test for end of queue
  if q.writeframe() == '':
    q.printqueue()
    print "Seconds Elapsed:",(time.time()-scriptstart)
    exit()  
