#! /usr/bin/env python3

import sys, os, warnings, time
from pyorbit import Device
from pyorbit import ConnectError
from pyorbit.services import PKI

def main(args):
    if len(args) < 3:
        print('Usage: pki_priv_key.py <device> <devuser> <devpass>')
        return

    try:
        host=args[0]
        username=args[1]
        password=args[2]
        
        dev = Device(host=host,username=username,password=password)
        dev.open()
        with PKI(dev) as pki:
            rsp = pki.get_priv_keys()
            print(rsp)
            #pki.cancel_priv_key_gen()
            pki.gen_priv_key(key_id="DEVKEY",key_size="2048")
            done = False
            while not done:
                status = pki.get_priv_key_gen_status()
                print(status)
                state = status['data']['pki']['private-keys']['generate-status']['state']
                if state in ['inactive', 'complete', 'cancelled', 'failed']:
                  done = True
                else:
                  time.sleep(5)
            rsp = pki.get_priv_keys()
            print(rsp)
            pki.del_priv_key(key_id="DEVKEY")
            rsp = pki.get_priv_keys()
            print(rsp)
    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
        return

if __name__ == '__main__':
    main(sys.argv[1:])
