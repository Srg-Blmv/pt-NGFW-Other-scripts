import requests
import random
from ipaddress import IPv4Address
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)




global_gr_id = ""
cookies = ""
headers = {"Content-Type": "application/json"}


def auth():
    global global_gr_id, cookies
    
    url = f"https://{mgmt_ip}/api/v2/Login"
    payload = {
        "login": mgmt_login,
        "password": mgmt_pass
    }
    
    response_auth = requests.post(url, json=payload, headers=headers, verify=False)
    if response_auth.status_code == 200:
        print("auth ok")
        payload = {}
        url =  f"https://{mgmt_ip}/api/v2/GetDeviceGroupsTree"
        r = requests.post(url, headers=headers, json=payload, verify=False, cookies=response_auth.cookies)
        cookies = response_auth.cookies
        # ПОЛУЧАЕМ ID глобальной группы
        global_gr_id = get_id_groupe(r.json()['groups'][0])

    else:
        print("auth fail")
        exit()


def get_id_groupe(groups):
    # Проверка текущей группы
    if groups.get("name") == groupe_name:
        return groups.get("id")
    # Проверка вложенных групп, если они существуют
    if "subgroups" in groups:
        for subgroup in groups["subgroups"]:  # Проходим по списку подгрупп
            result = get_id_groupe(subgroup)
            if result:  # Если id найдено, возвращаем его
                return result
    return None  # Возвращаем None, если ничего не найдено



def get_ip():
    # ---------------------  GET IP ----------------------
    url = f"https://{mgmt_ip}:443/api/v2/ListNetworkObjects"
    payload = {
        "deviceGroupId": global_gr_id,
        "objectKinds": ["OBJECT_NETWORK_KIND_IPV4_ADDRESS"],
        "offset": 0,
        "limit": 50000
    }

    response = requests.request("POST", url, json=payload, headers=headers, cookies=cookies, verify=False)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code} - {response.text}")
        exit()


def get_service():
    # ---------------------  GET SERVICE ----------------------
    url = f"https://{mgmt_ip}:443/api/v2/ListServices"

    payload = {
        "deviceGroupId": global_gr_id,
    
        "objectOriginKinds": ["OBJECT_ORIGIN_KIND_PREDEFINED"],
        "offset": 0,
        "limit": 10000
    }


    s = ['HTTPS-default-port', 'NFS-TCP-default-port', 'HTTP-default-port', 'NETBIOS-session-default-port', 'DNS-UDP-default-port','SMTP-default-port', 'POP3-default-port', 'IMAP-default-port', 'SIP-UDP-default-port', 'RDP-default-port', 'SYSLOG-UDP-default-port', 'SSH-default-port'  ]
    service_id = []
    response = requests.request("POST", url, json=payload,  headers=headers, cookies=cookies, verify=False)
    
    if response.status_code == 200:
        data = response.json()
        for service in data['services']:
            if service['name'] in s:
                service_id.append(service['id'])
        return service_id
    else:
        print(f"Error: {response.status_code} - {response.text}")
        exit()


def get_zones():
# ---------------------  GET ZONES ----------------------

    url = f"https://{mgmt_ip}:443/api/v2/ListZones"

    payload = {
        "offset": 0,
        "limit": 10000
    }

    response = requests.request("POST", url, json=payload,  headers=headers, cookies=cookies, verify=False)

    if response.status_code == 200:
        data = response.json()
        zones = [item["id"] for item in data["zones"] if not item["name"].startswith("Local")]
        return zones
        #print(zones)
    else:
        print(f"Error: {response.status_code} - {response.text}")
        exit()

    
    
def gen_list_ip(start_ip, end_ip ):
  start = int(IPv4Address(start_ip))
  end = int(IPv4Address(end_ip))
  all_ip = [str(IPv4Address(ip)).replace('.', '_') for ip in range(start, end + 1)]

  return all_ip



def find_id_by_name(data, name):
    for item in data['addresses']:
        if item['name'] == name:
            return item['id']
    return None


def random_rules():
  i = 0
  auth()
  possible_action = ["SECURITY_RULE_ACTION_DROP", "SECURITY_RULE_ACTION_ALLOW", "SECURITY_RULE_ACTION_DENY","SECURITY_RULE_ACTION_RESET_SERVER","SECURITY_RULE_ACTION_RESET_CLIENT","SECURITY_RULE_ACTION_RESET_BOTH"]
  possible_log = ["SECURITY_RULE_LOG_MODE_NO_LOG", "SECURITY_RULE_LOG_MODE_AT_SESSION_START", "SECURITY_RULE_LOG_MODE_AT_SESSION_END", "SECURITY_RULE_LOG_MODE_AT_RULE_HIT", "SECURITY_RULE_LOG_MODE_AT_SESSION_START_AND_END"]
  
    
  url_serv  = f"https://{mgmt_ip}/api/v2/CreateSecurityRule" 
  dump_ip = get_ip()
  ip_dict = {item['name']: item['id'] for item in dump_ip['addresses']}

  id_dict_services = get_service()

 
  net_48 = gen_list_ip("48.0.0.1", "48.0.9.196")
  net_49 = gen_list_ip("49.0.0.1", "49.0.9.196")
  net_50 = gen_list_ip("50.0.0.1", "50.0.9.196")
  net_51 = gen_list_ip("51.0.0.1", "51.0.9.196")  
  all_ip = net_48 + net_49 + net_50 + net_51



  for i, ip_name in enumerate(all_ip):
    ip_id = ip_dict.get(ip_name)  
    service = id_dict_services[i % len(id_dict_services)]
    payload = {
    "deviceGroupId": global_gr_id,
    "precedence": "pre",
    "position": i + 1,
    "enabled": True,
    "name": f"Random_Rule_{i}",
    "description": "",
    "sourceZone": {
        "kind": "RULE_KIND_ANY",
    },
    "destinationZone": {
        "kind": "RULE_KIND_ANY",
    },
    "sourceAddr": {
        "kind": "RULE_KIND_ANY",

    },
    "destinationAddr": {
        "kind": "RULE_KIND_LIST",
        "objects": {
            "array": [
                ip_id
            ]
        }
    },
    "sourceUser": {
        "kind": "RULE_USER_KIND_ANY",
        "objects": {}
    },
    "service": {
        "kind": "RULE_KIND_LIST",
        "objects": {
            "array": [
                service
            ]
        }
    },
    "application": {
        "kind": "RULE_KIND_ANY",
        "objects": {}
    },
    "urlCategory": {
        "kind": "RULE_KIND_ANY",
        "objects": {}
    },
    "action": "SECURITY_RULE_ACTION_ALLOW",
    "logMode": "SECURITY_RULE_LOG_MODE_AT_RULE_HIT"
    }
    
    #print(payload)
    
    headers = {"Content-Type": "application/json"}
    response_ser = requests.post(url_serv, json=payload, headers=headers, verify=False, cookies=cookies)
    print(f"Random_Rule_{i}: {response_ser.json()}")




mgmt_ip = "192.168.1.100"
mgmt_login =  "admin"
mgmt_pass = "xxXX1234$"
groupe_name= "Global"


random_rules()