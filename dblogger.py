#!/usr/bin/python

import time
writestart =  time.time()
format = '%x %X'
import csv
import ConfigParser

cfg = ConfigParser.ConfigParser()
cfg.read('brybus.cfg')
serialport = cfg.get('brybus','serialport')
database = cfg.get('db','database')
mysql_host = cfg.get('db','mysql_host')
mysql_user = cfg.get('db','mysql_user')
mysql_pass = cfg.get('db','mysql_pass')
mysql_db = cfg.get('db','mysql_db')

import _mysql
db=_mysql.connect(mysql_host,mysql_user,mysql_pass,mysql_db)

'''
Use this SQL code to create the table to log data to:

CREATE TABLE `data` (
	`ts` DATETIME NOT NULL,
	`request` VARCHAR(25) NULL DEFAULT NULL,
	`response` VARCHAR(350) NULL DEFAULT NULL,
	INDEX `ts` (`ts`)
)
'''


import brybus
ByteToHex = brybus.ByteToHex
HexToByte = brybus.HexToByte

def scantable():
  #make queue for 3b table  
  scan_q = brybus.writequeue()
  
  print "Building Queue"

  #table 3c isn't complete so use this array of valid rows
  table_3c = (
  '200130010300000B003C01',
  '200130010300000B003C03',
  '200130010300000B003C04',
  '200130010300000B003C05',
  '200130010300000B003C06',
  '200130010300000B003C08',
  '200130010300000B003C09',
  '200130010300000B003C0A',
  '200130010300000B003C0B',
  '200130010300000B003C0C',
  '200130010300000B003C0D',
  '200130010300000B003C0E',
  '200130010300000B003C0F',
  '200130010300000B003C10',
  '200130010300000B003C11',
  '200130010300000B003C12',
  '200130010300000B003C13',
  '200130010300000B003C14',
  '200130010300000B003C1E',
  '200130010300000B003C1F',
  '200130010300000B003C28',
  '200130010300000B003C29'
  )


  for r in range(1,16):
    reg = '00' + '3B' + "{0:02X}".format(r)
    f = brybus.frame(reg,'C','2001','3001','0B')
    scan_q.pushframe(f)
  #use the list above
  for r in table_3c:
    f = brybus.frame(r,'S')
    scan_q.pushframe(f)
  for r in range(1,4):
    reg = '00' + '3D' + "{0:02X}".format(r)
    f = brybus.frame(reg,'C','2001','3001','0B')
    scan_q.pushframe(f)
        
  return scan_q  

#=======main========

q = scantable()
#q.printqueue()

#setup the stream and bus
s = brybus.stream('S',serialport)
b = brybus.bus(s)

table=[]

query = "insert into data values (now(),'START','START')"
db.query(query)

while(1):
  #get write frame and write it 
  #write blocks, writes if the timeout passes, but returns without writing if data is received on the serial port
  wf_raw = q.writeframe()
  w = b.write(wf_raw)
  
  f = brybus.frame(b.read(),"B")
  if w==1:
    print "write", q.printstatus()
    #print wf.dst,wf.src,wf.len,wf.func,wf.data,wf.crc
    #print f.dst,f.src,f.len,f.func,f.data,f.crc

  #check the frame that was read against the queue to match the response with the request
  q.checkframe(f)
 
  #test for end of queue, then restart the queue
  if q.writeframe() == '':
    print "Seconds Elapsed:",(time.time()-writestart)
    writestart =  time.time()
    for k,v in q.queue.iteritems():
      v.done = False    
  
  found = 0
  for row in table:
    if row[0] == ByteToHex(f.raw[0:11]):
      if row[1] == f.data[6:]:
        1==1 #no change
        #print "NC", time.strftime(format), ByteToHex(f.raw[0:11]),f.data[6:]
      else:
        row[1]=f.data[6:]
        query = "insert into data values (now(),'"+ByteToHex(f.raw[0:11])+"','"+f.data[6:]+"')"
        db.query(query)
        print " C", time.strftime(format), ByteToHex(f.raw[0:11]),f.data[6:]
      found=1

  if found==0 and (f.func in ('0C','06')):
    table.append([ByteToHex(f.raw[0:11]),f.data[6:]])
    query = "insert into data values (now(),'"+ByteToHex(f.raw[0:11])+"','"+f.data[6:]+"')"
    db.query(query)
    print " A",time.strftime(format), ByteToHex(f.raw[0:11]),f.data[6:]

