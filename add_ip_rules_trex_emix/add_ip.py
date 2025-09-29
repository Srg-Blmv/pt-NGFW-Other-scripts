import requests
import random
import ipaddress
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)




global_gr_id = ""
cookies = ""

def auth():
    global global_gr_id, cookies

    url = f"https://{mgmt_ip}/api/v2/Login"
    headers = {"Content-Type": "application/json"}
    
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
        # Или заберите нужное ID через web api интерфейс: https://IP_MGMT/apidoc/v2/ui/#tag/device-groups/POST/api/v2/GetDeviceGroupsTree

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

def random_ip():
  auth()
  url_serv  = f"https://{mgmt_ip}/api/v2/CreateNetworkObject"


  ranges = [
    ('48.0.0.1', '48.0.9.196'),
    ('49.0.0.1', '49.0.9.196'), 
    ('50.0.0.1', '50.0.9.196'),
    ('51.0.0.1', '51.0.9.196')
    ]

  
  x = 0 
  for start_ip, end_ip in ranges:
    start = int(ipaddress.IPv4Address(start_ip))
    end = int(ipaddress.IPv4Address(end_ip))
    all_ips = [str(ipaddress.IPv4Address(ip)) for ip in range(start, end + 1)]
    for i in all_ips:
        x = x + 1
        payload_serv = {
            "name": f"{i.replace('.', '_')}",
            "deviceGroupId": global_gr_id,
            "description": "",
            "value": {
            "inet": {
                "inet": f"{i}/32"
            }
        }
        }
        #print(payload_serv)
        headers = {"Content-Type": "application/json"}
        response_ser = requests.post(url_serv, json=payload_serv, headers=headers, verify=False, cookies=cookies)
        print(f"{x}: {response_ser.json()}")



mgmt_ip = "192.168.1.100"
mgmt_login =  "admin"
mgmt_pass = "xxXX1234$"
groupe_name= "Global"

random_ip()