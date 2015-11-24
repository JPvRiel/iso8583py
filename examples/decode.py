import string
import argparse
import traceback
import sys

from ISO8583 import ISO8583
from ISOErrors import *

parser = argparse.ArgumentParser()
parser.add_argument("-D", "--debug", help="Enable debug", action="store_true", default=False)
parser.add_argument("-i", "--isoVersion", help="ISO version (year)", type=int, choices=[1987, 1993], default=1987)
parser.add_argument("ISO8583_ASCII_Message")

args = parser.parse_args()

print ('Message length: %i bytes' % len(args.ISO8583_ASCII_Message))

try:

  iso = ISO8583(args.ISO8583_ASCII_Message,version=args.isoVersion,debug=args.debug)  #debug on or off
  print ('MTI: %s' % iso.getMTI())
  print ('bitmap: %s' % iso.getBitmap())
  bits = iso.getBitsAndValues()
  print "bits present: " + ", ".join(str(b['bit']) for b in bits)
  for b in bits:
    print "[%s] %s (type %s %s, limit %s) = '%s'" % (b['bit'],iso.getLargeBitName(int(b['bit'])),b['type'],iso.getBitValueType(int(b['bit'])),iso.getBitLimit(int(b['bit'])),b['value'])

except (InvalidIso8583, BitInexistent, BitNotSet, InvalidBitType, InvalidMTI, InvalidValueType, ValueToLarge) as err:
  print "\nERROR. ISO8583 library exception"
  print "Exception: %s" % err.__class__.__name__
  print "Message: %s" % err
