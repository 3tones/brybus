import csv  

import brybus

from curses.ascii import isprint

def printable(input):
    return ''.join(char for char in input if isprint(char))
  
  
def main():  
  #load CSV into memory
  data = []
  tfin = csv.reader(open('mydata.txt', 'rb'), delimiter=' ')
  for row in tfin:
    f = brybus.frame(row[2],"S")
    s = printable(f.data.decode('hex'))
    if s != '':
      print f.src,f.data[:6],s
      
    
    
main()