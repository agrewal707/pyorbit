#! /usr/bin/env python3

import sys, os, warnings, time, json
from pyorbit import Device
from pyorbit import ConnectError
from pyorbit.services import CellFirmware

def get_carrier_version(rsp, carrier):
  vers = rsp['data']['interfaces-state']['interface']['firmware']['versions']
  for ver in vers:
      #print(ver)
      if carrier in ver['version']:
          return ver

def main(args):
    if len(args) < 4:
        print('Usage: delete_cell_firmware.py <device> <devuser> <devpass> <carrier>')
        return

    try:
        host=args[0]
        username=args[1]
        password=args[2]
        carrier=args[3]
        
        dev = Device(host=host,username=username,password=password)
        dev.open()
        with CellFirmware(dev) as fw:
            rsp = fw.get_versions(ifname='Cell')
            #print(json.dumps(rsp))
            ver = get_carrier_version(rsp, carrier)
            print("CURRENT VERSION: {}".format(json.dumps(ver)))
            id = ver['id'];
            fw.delete(ifname='Cell', id=id)
            #fw.restart(ifname='Cell', id=id)
    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
        return

if __name__ == '__main__':
    main(sys.argv[1:])
