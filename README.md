brybus
======
brybus is a set of python packages and scripts to provide a framework to communicate on a Bryant Evolution or Carrier Infinity communications bus.

brybus.py provides a stream and bus class to attach to a data source and deal with timing and framing.  It also provides a queue for frames to put on the bus.

readraw.py is a sample script showing the use of the classes.

scandevtable.py takes a multi phase approach to scan your entire bus looking for valid data registers, and outputs that information to myregisters.csv.

scanalldata.py uses myregisters.csv to read all valid data registers, and outputs that information to mydata.txt.

tableascii.py reads mydata.txt and outputs any valid ASCII data.

Requirements
============
http://pyserial.sourceforge.net/

curses module for tableascii.py

mysql support in python for data logging (script not posted yet)
