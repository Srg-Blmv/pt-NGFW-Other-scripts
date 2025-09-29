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

`add_ip_rules_trex_emix` - %username% Проверяли логирование на большом количестве правил, задача что бы трафик выходил не по одному правилу. В конце any any.
```
правила МСЭ:
Any to 48.0.0.1 port 443 tcp allow
Any to 48.0.0.2 port 2049 tcp allow
Any to 48.0.0.3 port 80 tcp allow 
Any to 48.0.0.4 port 139 tcp allow
Any to 48.0.0.5 port 53 udp allow
Any to 48.0.0.6 port 25 tcp allow
Any to 48.0.0.7 port 110 tcp allow
Any to 48.0.0.8 port 143 tcp allow
Any to 48.0.0.9 port 5060 udp allow
Any to 48.0.0.10 port 3389 udp allow
Any to 48.0.0.11 port 514 udp allow
Any to 48.0.0.12 port 22 allow

далее циклически повторяются порты с начала.
Any to 48.0.0.13 port 443 tcp allow
Any to 48.0.0.14 port 2049 tcp allow
Any to 48.0.0.15 port 80 tcp allow
….
и так по всем адресам:
48.0.0.1-48.0.9.196
49.0.0.1-49.0.9.196
50.0.0.1-50.0.9.196
51.0.0.1-51.0.9.196
```
---