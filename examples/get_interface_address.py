#! /usr/bin/env python3

import sys, os, warnings

from pyorbit import Device
from pyorbit import ConnectError
from pyorbit.services import Status

def main(host, user, passwd, ifname):
    try:
        dev = Device(host=host,username=user,password=passwd)
        dev.open()
        with Status(dev) as st:
            ipv4="""/interfaces-state/interface[name='{}']/ipv4/address""".format(ifname)

            # JSON
            out = st.get(filter=('xpath',ipv4),format='json')
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
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
