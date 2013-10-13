#!/usr/bin/python

import serial  #need this added from base python package
import crcmod  #need this added from base python package
import struct
import time

import bryfunc
ByteToHex = bryfunc.ByteToHex
HexToByte = bryfunc.HexToByte



class stream:
  'connect to a file or serial port'
  
  def __init__(self,type,path):
    self.type = type
    self.path = path
    
    if self.type == "S":
      self.ser = serial.Serial(self.path,38400)
      print "Opening ",self.ser.portstr
      
    #TODO add type for file stream
    
  def read(self, bytes):
    return self.ser.read(bytes)

  def write(self, data):
    self.ser.write(data)
  
  def inWaiting(self):
    return self.ser.inWaiting()

class bus:
  'functions to read/write from the carrier/bryant bus'
  #attatches to the stream and handles specifics of timing and framing

  def __init__(self,stream):
    self.stream = stream
    self.locked = 0
    self.starttime = 0
    self.timetrigger = False
    self.lastfunc = ''
    self.timeout = 0.03
  
  def read(self):
    head = self.stream.read(8)

    #check to make sure we're looking at the header
    while not self.locked:
      self.locked = 0
      if head[1]=='\x01' or head[1]=='\xF1':
        if head[3]=='\x01':
          if head[5]=='\x00' and head[6]=='\x00':
            self.locked = 1
      if self.locked == 0:
        print "not locked - discarding 1 byte"
        head = head[1:]
        head += self.stream.read(1)
    
    #set lastfunc for testing before write
    self.lastfunc = ByteToHex(head[7])
    #get the length to read from the header
    readlen = int(ByteToHex(head[4]),16)
    #read len+2 for data and checksum (the rest of the frame)
    data = self.stream.read(2+readlen)  
    return head + data
  
  def write(self,data):
    #blocking call to test when it is ok to write - then write if OK
    #return 0 = no action
    #return 1 = item written
    #return 2 = paused, but no write
    
    #mark the current time
    self.starttime = time.clock()
    self.timetrigger=True
  
    #wait for data to become available - inWaiting is non blocking
    self.pause = False
    self.writeok = False
    while not self.inWaiting():
      if self.timetrigger and ((self.starttime + self.timeout) < time.clock()) and (self.lastfunc=='06'):
        self.pause=True
        if data != '':
          #TODO add "safe mode" to block invalid functions
          self.stream.write(data)
          self.writeok=True
        self.timetrigger=False
    if self.writeok:
      return 1
    if self.pause:
      return 2
    return 0
    
  def inWaiting(self):
    return self.stream.inWaiting()

class frame:
  'this class represents a frame from the bus'
  
  def __init__(self,data,type,dst='',src='',func=''):
    if type == "B": #binary
      self.raw = data
    if type == "S": #string
      self.raw = HexToByte(data)
    if type == "C": #create frame
      self.len_int = len(data)/2
      self.len = "{0:02X}".format(self.len_int)
        #formatting string:
        #0: first parameter
        #0  fill with zeros
        #2  fill to n chars
        #x  hex, uppercase
      self.raw = HexToByte(dst + src + self.len + '0000' + func + data) 

    #parse out the parts of the frame  
    self.dst = ByteToHex(self.raw[0:2])
    self.src = ByteToHex(self.raw[2:4])
    self.len = ByteToHex(self.raw[4])
    self.len_int = int(self.len,16)
    self.func = ByteToHex(self.raw[7])
    self.ts = time.clock()
    
    self.crc16 = crcmod.predefined.Crc('crc-16').new()

    #Note: the length of the entire frame minus 8 for the header, and 2 for the crc should be the length given in the frame
    if len(self.raw)-8-2 == self.len_int:
      #if this frame already has a CRC, check it
      self.data = ByteToHex(self.raw[8:8+self.len_int])
      self.crc = ByteToHex(self.raw[8+self.len_int:]) 
      #check crc
      self.crc16.update(self.raw[:8+self.len_int])
      self.crccalc = ByteToHex(struct.pack('<H',self.crc16.crcValue))
      #TODO put a flag for valid CRC
    else:
      #if it does not have a CRC, add it (used when making frames)
      self.crc16.update(self.raw)
      self.crc = ByteToHex(struct.pack('<H',self.crc16.crcValue)) 
      self.raw += struct.pack('<H',self.crc16.crcValue)
      self.data = ByteToHex(self.raw[8:8+self.len_int])

  def print_str(self):
    return ByteToHex(self.raw)
