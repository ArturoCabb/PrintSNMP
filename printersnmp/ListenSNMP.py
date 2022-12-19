import argparse
from pysnmp.entity.rfc3413.oneliner import cmdgen
import time
import SaveData

if  __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Te input value is")
    parser.add_argument('--ip', nargs='?', help='The target ip address', required=True)
    parser.add_argument('--communityIndex', nargs='?', help='The community index', required=False, default='public')
    parser.add_argument('--communityGroup', nargs='?', help='The community group', required=False, default='public')
    parser.add_argument('--oid', nargs='?', help='The object identifier of the target like 1.3.6.1.2.1.25.3.5.1', required=False, default='1.3.6.1.2.1.25.3.5.1')
    parser.add_argument('--version', nargs='?', help='The SNMP version of the target [v1, v2, v3]', required=True)
    inputArgs = parser.parse_args()
    
    version = 1
    if (inputArgs.version == 'v1'):
        version = 0
    elif (inputArgs.version == 'v2'):
        version = 1
    elif (inputArgs.version == 'v3'):
        version = 2
    
    print("Esc to exit")
    
    while True:
        errorIndication, errorStatus, errorIndex, \
        varBindTable = cmdgen.CommandGenerator().bulkCmd(  
                    cmdgen.CommunityData(communityIndex= inputArgs.communityIndex, communityName= inputArgs.communityGroup, mpModel= version),  
                    cmdgen.UdpTransportTarget((inputArgs.ip, 161)),  
                    0,
                    25, 
                    (inputArgs.oid), # ipAddrTable OID . This works fine. .1.3.6.1.2.1.25.3.5.1.2.1 1.3.6.1.2.1.1.1.0
                )
    
        if errorIndication:
           print(errorIndication)
        else:
            if errorStatus:
                print('%s at %s\n' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                    ))
            else:
                for varBindTableRow in varBindTable:
                    for name, val in varBindTableRow:
                        SaveData.saveFile(('%s = %s\n' % (name.prettyPrint(), val.prettyPrint())))
                        print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
        time.sleep(2)