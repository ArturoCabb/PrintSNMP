from pysnmp import hlapi
import argparse
from datetime import datetime

def saveFile(value):
    date = datetime.today().strftime('%Y-%m-%d')
    file = open(date + ".txt" ,"a+")
    file.write(value)
    file.close

def get(target, oids, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.getCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        *construct_object_types(oids)
    )
    return fetch(handler, 1)[0]

def construct_object_types(list_of_oids):
    object_types = []
    for oid in list_of_oids:
        object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
    return object_types

def fetch(handler, count):
    result = []
    for i in range(count):
        try:
            error_indication, error_status, error_index, var_binds = next(handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    items[str(var_bind[0])] = cast(var_bind[1])
                result.append(items)
            else:
                raise RuntimeError('Got SNMP error: {0}'.format(error_indication))
        except StopIteration:
            break
    return result

def cast(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        try:
            return float(value)
        except (ValueError, TypeError):
            try:
                return str(value)
            except (ValueError, TypeError):
                pass
    return value

parser = argparse.ArgumentParser(description="Te input value is")
parser.add_argument('--ip', nargs='?', help='The target ip address', required=True)
parser.add_argument('--community', nargs='?', help='The community group', required=True)
parser.add_argument('--oid', nargs='?', help='The object identifier of the target', required=True)
parser.add_argument('--version', nargs='?', help='The version of SNMP of the target [v2, v3]', required=True)
parser.add_argument('--user', nargs='?', help='The user session', required=False)
parser.add_argument('--authenticationkey', nargs='?', help='The authentication key', required=False)
parser.add_argument('--encryptionkey', nargs='?', help='The encryption key', required=False)
inputArgs = parser.parse_args()

print("Clrl + c to exit")

if (inputArgs.version == "v2"):
    value = get(inputArgs.ip, [inputArgs.oid], hlapi.CommunityData(inputArgs.community))
    saveFile(value)
    print(value)
elif (inputArgs.version == "v3"):
    value = get(inputArgs.ip, [inputArgs.oid], hlapi.UsmUserData(inputArgs.user, authKey=inputArgs.authenticationkey, privKey=inputArgs.encryptionkey, authProtocol=hlapi.usmHMACSHAAuthProtocol, privProtocol=hlapi.usmAesCfb128Protocol))
    saveFile(value)
    print(value)
else:
    print("Specify a snmp version")