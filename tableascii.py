import csv  

import brybus
import ConfigParser

cfg = ConfigParser.ConfigParser()
cfg.read('brybus.cfg')
scan_data = cfg.get('scanner','scan_data')

from curses.ascii import isprint

def printable(input):
    return ''.join(char for char in input if isprint(char))
  
  
def main():  
  #load CSV into memory
  data = []
  tfin = csv.reader(open(scan_data, 'rb'), delimiter=' ')
  for row in tfin:
    f = brybus.frame(row[2],"S")
    s = printable(f.data.decode('hex'))
    if s != '':
      print f.src,f.data[:6],s
      
    
    
main()
