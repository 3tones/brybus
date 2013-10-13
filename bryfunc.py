#!/usr/bin/python

#==================== AUX FUNCTIONS ===================
#from http://code.activestate.com/recipes/510399-byte-to-hex-and-hex-to-byte-string-conversion/

def ByteToHex( byteStr ):
	return ''.join( [ "%02X" % ord( x ) for x in byteStr ] ).strip()

def HexToByte( hexStr ):
  bytes = []
  hexStr = ''.join( hexStr.split(" ") )
  for i in range(0, len(hexStr), 2):
    bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )
  return ''.join( bytes )
