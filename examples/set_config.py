#! /usr/bin/env python

import sys, os, warnings
from pyorbit import Device
from pyorbit import ConnectError
from pyorbit.services import Config

config="""
<config>
    <system xmlns="urn:ietf:params:xml:ns:yang:ietf-system">
        <ntp>
            <use-ntp>true</use-ntp>
            <ntp-server>
                <address>1.1.1.1</address>
            </ntp-server>
        </ntp>
    </system>
</config>
"""

def main(host, user, passwd):
    try:
        dev = Device(host=host,username=user,password=passwd)
        dev.open()
        with Config(dev) as cm:
            rsp = cm.load(content=config)
            print(rsp)
            rsp = cm.validate()
            print(rsp)
            rsp = cm.commit()
            print(rsp)
    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
        return

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
