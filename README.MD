`delete_obj_by_name.py`: Удаляет один объект по имени

---

`add_ip_from_file_txt > add_IP_from_txt.py`: Добавляет IP/net/fqdn из txt в объекты,  **создает новую** группу и добавляет объекты в нее.

---

`change_name_rules.py` - Проходит по всем правилам и изменяет в них имя. в данном примере заменяем `_copy_` на `_`

```python
    for item in data['items']:
        if '_copy_' in item['name']:
            name = item['name'].replace("_copy_", "_")
# ("_copy_", "_")
# _copy_  строка которую ищем в имени файла если находим то меняем на _

```

---