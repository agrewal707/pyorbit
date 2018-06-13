#! /usr/bin/env python3

import sys, os, warnings, time
from pyorbit import Device
from pyorbit import ConnectError
from pyorbit.services import Config,PKI

cert_server_config="""
<config>
    <pki xmlns="com:gemds:mds-certmgr">
        <certificate-servers>
            <certificate-server>
                <cert-server-identity>{}</cert-server-identity>
                <server-type>scep</server-type>
                <server-setting xmlns="com:gemds:mds-certmgr-servers">
                  <uri>{}</uri>
                  <digest-algo>{}</digest-algo>
                  <encrypt-algo>{}</encrypt-algo>
                </server-setting>
            </certificate-server>
        </certificate-servers>
    </pki>
</config>
"""

ca_server_config="""
<config>
  <pki xmlns="com:gemds:mds-certmgr">
  <ca-servers>
    <ca-server>
      <ca-issuer-identity>{}</ca-issuer-identity>
      <ca-fingerprint>{}</ca-fingerprint>
    </ca-server>
  </ca-servers>
  </pki>
</config>
"""

cert_info_config="""
<config>
  <pki xmlns="com:gemds:mds-certmgr">
  <cert-info>
    <certificate-info>
      <certificate-info-identity>{}</certificate-info-identity>
      <country-x509>{}</country-x509>
      <state-x509>{}</state-x509>
      <locale-x509>{}</locale-x509>
      <organization-x509>{}</organization-x509>
      <org-unit-x509>{}</org-unit-x509>
      <common-name-x509>{}</common-name-x509>
      <pkcs9-email-x509>{}</pkcs9-email-x509>
    </certificate-info>
  </cert-info>
  </pki>
</config>
"""

def main(args):
    if len(args) < 3:
        print('Usage: pki_scep.py <device> <devuser> <devpass>')
        return

    try:
        host=args[0]
        username=args[1]
        password=args[2]
        
        dev = Device(host=host,username=username,password=password)
        dev.open()
        with Config(dev) as cm:
            # Configure certificate server
            print("CONFIGURING CERT SERVER...")
            cfg = cert_server_config.format("CERT-SERVER", "10.15.60.39/certsrv/mscep/mscep.dll", "md5", "des_cbc")
            rsp = cm.load(content=cfg)
            print(rsp)
            rsp = cm.validate()
            print(rsp)
            # Configure CA server
            print("CONFIGURING CA CERT SERVER...")
            cfg = ca_server_config.format("CA-SERVER", "5E2F7B923EDA99A7ADB814A0E3FFF657")
            rsp = cm.load(content=cfg)
            print(rsp)
            rsp = cm.validate()
            print(rsp)
            # Configure Certificate Info
            print("CONFIGURING CERT INFO...")
            cfg = cert_info_config.format("CERT-INFO", "US", "NY", "Rochester", "GEMDS", "ENGG", "DEVICE-1", "DEVICE-1@ge.com")
            rsp = cm.load(content=cfg)
            print(rsp)
            rsp = cm.validate()
            print(rsp)
            # Commit configuration
            print("COMMITING CONFIG...")
            rsp = cm.commit()
            print(rsp)
        with PKI(dev) as pki:
            rsp = pki.get_priv_keys()
            print(rsp)
            # Generate private key
            print("GENERATING PRIVATE KEY...")
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
            rsp = pki.get_ca_certs()
            print(rsp)
            print("IMPORT CA CERTS...")
            pki.import_ca_cert_scep(cert_id="CACERT",cert_server_id="CERT-SERVER",ca_server_id="CA-SERVER")
            done = False
            while not done:
                status = pki.get_ca_cert_import_status()
                print(status)
                state = status['data']['pki']['ca-certs']['import-status']['state']
                if state in ['inactive', 'complete', 'cancelled', 'failed']:
                  done = True
                else:
                  time.sleep(5)
            rsp = pki.get_ca_certs()
            print(rsp)
            #pki.del_ca_cert(cert_id="CACERT")
            #rsp = pki.get_ca_certs()
            #print(rsp)

            rsp = pki.get_client_certs()
            print(rsp)
            print("IMPORT CLIENT CERTS...")
            pki.import_client_cert_scep(cert_id="DEVCERT",cert_server_id="CERT-SERVER",ca_server_id="CA-SERVER", cert_info_id="CERT-INFO",cacert_id="CACERT",key_id="DEVKEY",otp="4B7AC2AFC101104F06C88A174C88CD52")
            done = False
            while not done:
                status = pki.get_client_cert_import_status()
                print(status)
                state = status['data']['pki']['client-certs']['import-status']['state']
                if state in ['inactive', 'complete', 'cancelled', 'failed']:
                  done = True
                else:
                  time.sleep(5)
            rsp = pki.get_client_certs()
            print(rsp)
            #pki.del_ca_cert(cert_id="CACERT")
            #rsp = pki.get_ca_certs()
            #print(rsp)
    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
        return

if __name__ == '__main__':
    main(sys.argv[1:])
