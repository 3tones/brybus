#!/usr/bin/python

#an example program to use brybus and bryqueue
#writes to frames constructed differently and reads
#frames from the bus

import time
import brybus
import ConfigParser

cfg = ConfigParser.ConfigParser()
cfg.read('brybus.cfg')
serialport = cfg.get('brybus','serialport')

#build a frame if you already know it
f1 = brybus.frame('400130010300000B000101',"S")
print "Frame Built: ",f1.print_str()

#build a frame from parts: data, C for Create, dst, src, function
f2 = brybus.frame('000101','C','5001','3001','0B')
print "Frame Built: ",f2.print_str()

#build the queue and put the items in it
q = brybus.writequeue()
q.pushframe(f1)
q.pushframe(f2)
q.printqueue()

#setup the stream and bus
s = brybus.stream('S',serialport)
b = brybus.bus(s)

#loop forever
while(1):

  #write data if there
  b.write(q.writeframe())
  
  #read data
  f = brybus.frame(b.read(),"B") 

  #print the raw data in a nice format
  print f.dst,f.src,f.len,f.func,f.data,f.crc

