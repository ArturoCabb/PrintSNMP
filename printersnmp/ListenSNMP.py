import socket
import random
import argparse
from struct import pack, unpack
from datetime import datetime as dt
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto.rfc1902 import Integer, IpAddress, OctetString
from datetime import datetime

def saveFile(value):
    date = datetime.today().strftime('%Y-%m-%d')
    file = open(date + ".txt" ,"a+")
    file.write(value)
    file.close

parser = argparse.ArgumentParser(description="Te input value is")
parser.add_argument('--ip', nargs='?', help='The target ip address', required=True)
parser.add_argument('--community', nargs='?', help='The community group', required=True)
parser.add_argument('--oid', nargs='?', help='The object identifier of the target', required=True)
inputArgs = parser.parse_args()

while True:
    #ip = '192.168.1.60'
    #community = 'public'
    #value = "1.3.6.1.2.1.1.2.0"
    ip = inputArgs.ip
    community = inputArgs.community
    value = inputArgs.oid
    
    generator = cmdgen.CommandGenerator()
    comm_data = cmdgen.CommunityData(community)  # 1 means version SNMP v2c
    transport = cmdgen.UdpTransportTarget((ip, 161))

    real_fun = getattr(generator, 'getCmd')
    res = (errorIndication, errorStatus, errorIndex, varBinds) \
        = real_fun(comm_data, transport, value)

    if not errorIndication is None or errorStatus is True:
        print("Error: %s %s %s %s" % res)
    else:
        print("%s" % varBinds)
        saveFile(varBinds)