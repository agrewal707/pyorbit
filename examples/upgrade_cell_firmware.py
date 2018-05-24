#! /usr/bin/env python3

import sys, os, warnings, time, json
from pyorbit import Device
from pyorbit import ConnectError
from pyorbit.services import CellFirmware
from ncclient.operations.errors import TimeoutExpiredError

def get_carrier_version(rsp, carrier):
  vers = rsp['data']['interfaces-state']['interface']['firmware']['versions']
  for ver in vers:
      #print(ver)
      if carrier in ver['version']:
          return ver
  

def main(args):
    if len(args) < 7:
        print('Usage: upgrade_cell_firmware.py <device> <devuser> <devpass> <sftphost> <sftpuser> <sftppass> <sftpfilepath>')
        return

    try:
        host=args[0]
        username=args[1]
        password=args[2]
        sftp_host=args[3]
        sftp_username=args[4]
        sftp_password=args[5]
        sftp_filepath=args[6]
        
        dev = Device(host=host,username=username,password=password)
        dev.open()
        with CellFirmware(dev) as fw:
            rsp = fw.get_versions(ifname='Cell')
            #print(json.dumps(rsp))
            carrier = 'VERIZON'
            print("CURRENT VERSION: {}".format(json.dumps(get_carrier_version(rsp, carrier))))
            fw.cancel(ifname='Cell')
            url = 'sftp://{}{}'.format(sftp_host,sftp_filepath)
            fw.load(ifname='Cell', url=url, username=sftp_username, password=sftp_password)
            done = False
            while not done:
                try:
                    rsp = fw.status(ifname='Cell')
                    status = rsp['data']['interfaces-state']['interface']['firmware']['reprogram-status']
                    print("CURRENT STATUS: {}".format(json.dumps(status)))
                    state = status['state']
                    if state in ['complete', 'cancelled', 'failed']:
                        print("OPERATION STATE: {}".format(state))
                        rsp = fw.get_versions(ifname='Cell')
                        print("CURRENT VERSION: {}".format(json.dumps(get_carrier_version(rsp, carrier))))
                        done = True
                    else:
                        time.sleep(5)
                except TimeoutExpiredError as err:
                    print("request timedout")
                    time.sleep(5)
    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
        return

if __name__ == '__main__':
    main(sys.argv[1:])
