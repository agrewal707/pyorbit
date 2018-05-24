#! /usr/bin/env python3

import sys, os, warnings
from pyorbit import Device
from pyorbit import ConnectError
from pyorbit.services import Config

def main(host, user, passwd):
    try:
        dev = Device(host=host,username=user,password=passwd)
        dev.open()
        with Config(dev) as cm:
            out = cm.get(format='json')
            print(out)
    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
        return

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
