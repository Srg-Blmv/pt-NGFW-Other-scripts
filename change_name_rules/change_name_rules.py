import requests
import json
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
        payload={}
        url =  f"https://{mgmt_ip}/api/v2/GetDeviceGroupsTree"
        r = requests.post(url, headers=headers, json=payload, verify=False, cookies=response_auth.cookies)
        cookies = response_auth.cookies
        # ПОЛУЧАЕМ ID глобальной группы
        global_gr_id = get_id_groupe(r.json()['groups'][0])
        # Пример 1 группы в глобальной:
        #global_gr_id = (r.json()['groups'][0].get("subgroups")[0].get('id'))
        # Или заберите нужное ID через web api интерфейс: https://IP_MGMT/apidoc/v2/ui/#tag/device-groups/POST/api/v2/GetDeviceGroupsTree
        # сохраним имя группы для 
        
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


def main():
    auth()
    url_main  = f"https://{mgmt_ip}/api/v2/ListSecurityRules"
    url__update_rule  = f"https://{mgmt_ip}/api/v2/UpdateSecurityRule"
    headers = {"Content-Type": "application/json"}
    
    payload_list_url = {
            "limit": 10000,
            "deviceGroupId": f"{global_gr_id}",
            "precedence": precedence
        }  
    response_ser = requests.post(url_main, json=payload_list_url, headers=headers, verify=False, cookies=cookies)
    
    if response_ser.status_code == 200:
        data = response_ser.json()




    def get_service(obj):
        id_list = []   
        if obj['kind'] == "RULE_KIND_LIST":
            for o in obj['objects']:
                for key in o:
                    if 'id' in o[key]:
                        id_list.append(o[key]['id']) 
            return {
                "kind": "RULE_KIND_LIST",
                "objects": {"array": id_list}  # Добавить {"array": }
            }
        else:
            return {
                "kind": "RULE_KIND_ANY",
                "objects": {"array": []}
            }

    def get_id_zones(obj):
        id_list = []   
        if obj['kind'] == "RULE_KIND_LIST":
            for o in obj['objects']:
                if 'id' in o:
                    id_list.append(o['id'])
            return {
                "kind": "RULE_KIND_LIST",
                "objects": {"array": id_list}  # Добавить {"array": }
            }
        else:
            return {
                "kind": "RULE_KIND_ANY",
                "objects": {"array": []}
            }



    for item in data['items']:
        if '_copy_' in item['name']:
            name = item['name'].replace("_copy_", "_")
        
            payload = {
                "id": item['id'],
                "name": name,
                "description": item.get('description', ''),
                "sourceZone": get_id_zones(item['sourceZone']),
                "destinationZone": get_id_zones(item['destinationZone']),
                "sourceAddr": get_service(item['sourceAddr']),
                "destinationAddr": get_service(item['destinationAddr']),
                "service": get_service(item['service']),
                "sourceUser": {"kind": "RULE_USER_KIND_ANY", "objects": {"array": []}},
                "application": {"kind": "RULE_KIND_ANY", "objects": {"array": []}},
                "urlCategory": {"kind": "RULE_KIND_ANY", "objects": {"array": []}},
                "action": item.get('action'),
                "logMode": item.get('logMode'),
                "schedule": item.get('schedule', {}),
                "ipsProfileId": item.get('ipsProfileId', ''),
                "avProfileId": item.get('avProfileId', ''),
            }


            response = requests.post(url__update_rule, json=payload, headers=headers, verify=False, cookies=cookies)
            if response.status_code == 200:
                print(f"{item['name']} -> {name}")
            else:
                print(f"Error: {response.status_code}  :  {response.json()} ")
                print(payload)
                print("-----------")

        else:
            continue




mgmt_ip = "192.168.212.101"       # IP MGMT
mgmt_login =  "admin"           # LOGIN 
mgmt_pass = "xxXX1234$"         # Password
groupe_name = "Global"          # Имя группы
precedence = "pre"              # Pre or Post





main()                