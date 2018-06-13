#! /usr/bin/env python3

import sys, os, warnings, time
from pyorbit import Device
from pyorbit import ConnectError
from pyorbit.services import PKI

def main(args):
    if len(args) < 7:
        print('Usage: pki_fw.py <device> <devuser> <devpass> <sftphost> <sftpuser> <sftppass> <sftpfilepath>')
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
        with PKI(dev) as pki:
            rsp = pki.get_fw_certs()
            print(rsp)
            url = 'sftp://{}{}'.format(sftp_host,sftp_filepath)
            pki.import_fw_cert(cert_id="GEMDS-FW",url=url,username=sftp_username,password=sftp_password)
            done = False
            while not done:
                status = pki.get_fw_cert_import_status()
                print(status)
                state = status['data']['pki']['firmware-certs']['import-status']['state']
                if state in ['inactive', 'complete', 'cancelled', 'failed']:
                  done = True
                else:
                  time.sleep(5)
            rsp = pki.get_fw_certs()
            print(rsp)
            #pki.del_fw_cert(cert_id="GEMDS-FW")
            #rsp = pki.get_fw_certs()
            #print(rsp)
    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
        return

if __name__ == '__main__':
    main(sys.argv[1:])
