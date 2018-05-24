#! /usr/bin/env python3

import sys, os, warnings, time
from pyorbit import Device
from pyorbit import ConnectError
from pyorbit.services import Firmware,System

def main(args):
    if len(args) < 7:
        print('Usage: upgrade_firmware.py <device> <devuser> <devpass> <sftphost> <sftpuser> <sftppass> <sftpfilepath>')
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
        with Firmware(dev) as fw:
            rsp = fw.get_versions()
            print(rsp)
            fw.cancel()
            url = 'sftp://{}{}'.format(sftp_host,sftp_filepath)
            fw.load(url=url, username=sftp_username, password=sftp_password)
            done = False
            while not done:
                status = fw.status()
                print(status)
                state = status['data']['system']['firmware']['reprogram-status']['state']
                if state in ['complete', 'cancelled', 'failed']:
                  done = True
                else:
                  time.sleep(5)
        with System(dev) as sys:
            #sys.restart()
            #sys.restart(location=1)
            sys.restart(type='inactive')
            #sys.restart(version='6.7.8-M1')
            #sys.restart(version='6.1.2')
    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
        return

if __name__ == '__main__':
    main(sys.argv[1:])
