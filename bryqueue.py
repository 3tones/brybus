#!/usr/bin/python

import brybus

class queueitem:
  'a single item to put on the bus - used in the queue'
  def __init__(self,f):
    self.frame = f
    self.response = brybus.frame('000130010100000B000000','S')
    self.done = False
  
  def print_str(self):
    return self.frame.print_str()+' '+self.response.print_str()+' '+str(self.done)

class writequeue:
  'a queue to hold items and their responses to/from the bus'
  def __init__(self):
    self.queue = {}
    self.index = 0
  
  #put a new frame on the queue
  def pushframe(self,f):
    self.queue[self.index] = queueitem(f) 
    self.index+=1
    return self.index-1 
  
  #take any frame and see if it is a response
  #this should be checked immediatley after writing the frame for best results
  #this depends on writeframe() returing the same thing when it was called to write
  #  and the following frame is the response based on a swapped src/dst.
  #  this is the best we can do since an error can be a response and there is no for sure match
  def checkframe(self,frame):
    for k,v in self.queue.iteritems():
      if v.frame.src==frame.dst and v.frame.dst==frame.src and v.frame.raw==self.writeframe():
        v.response = frame
        v.done = True
        break
  
  #return raw frame to be written to the bus
  def writeframe(self):
    for k in sorted(self.queue.keys()):
      if self.queue[k].done==False:
        return self.queue[k].frame.raw
        break
    return ''
  
  #test function for to force all items done
  def test(self):
    for k,v in self.queue.iteritems():
      v.done = True    
  
  #TODO remove frame from queue
  #def popframe(self,index):
  
  #print the queue
  def printqueue(self):
    for k,v in self.queue.iteritems():
      print k,v.print_str()
  
  def printstatus(self):
    total = len(self.queue)
    done = 0
    for k,v in self.queue.iteritems():
      if v.done==True:
        done+=1
    return str(done)+'/'+str(total)
