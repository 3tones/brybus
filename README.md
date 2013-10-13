brybus
======
brybus is a set of python packages and scripts to provide a framework to communicate on a Bryant Evolution or Carrier Infinity communications bus.

brybus.py provides a stream and bus class to attach to a data source and deal with timing and framing.

bryqueue.py provides a queue of frames to put on the bus (used in scripts)

readraw.py is a sample script showing the use of the classes

scandevtable.py scans your entire bus looking for valid data registers

scanalltables.py uses the output from scandevtable.py to read all valid data registers
