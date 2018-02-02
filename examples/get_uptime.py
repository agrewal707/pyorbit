#! /usr/bin/env python

import sys, os, warnings

from pyorbit import Device
from pyorbit import ConnectError
from pyorbit.services import Status

# Example showing how to get the system uptime from an Orbit Radio.
# The uptime value is requested using it's keypath. The keypath
# can be obtained from the Orbit Radio command line using:
#   show system uptime | display xpath
#
# This will return the following keypath:
#   /system/mdssys:uptime/seconds 175198
#
# Strip off the namespace prefix 'mdssys' and we're left with:
#   /system/uptime/seconds
#
# Running this example and piping the output through 'jq'
# should produce JSON data like the following:
#
#   python3 pyorbit/examples/get_status.py 192.168.1.1 admin admin | jq
#   {
#     "data": {
#       "@xmlns": "urn:ietf:params:xml:ns:netconf:base:1.0",
#       "@xmlns:nc": "urn:ietf:params:xml:ns:netconf:base:1.0",
#       "system": {
#         "@xmlns": "urn:ietf:params:xml:ns:yang:ietf-system",
#         "uptime": {
#           "@xmlns": "com:gemds:mds-system",
#           "seconds": "175732"
#         }
#       }
#     }
#   }

def main(host, user, passwd):
    try:
        dev = Device(host=host,username=user,password=passwd)
        dev.open()
        with Status(dev) as st:
            uptime="""/system/uptime/seconds"""

            # JSON
            out = st.get(filter=('xpath',uptime),format='json')
            print(out)

            # ODICT
            #out = st.get(filter=('xpath',uptime),format='odict')
            #print(out)

            # XML
            #out = st.get(filter=('xpath',uptime))
            #print(out)

    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
        return

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
