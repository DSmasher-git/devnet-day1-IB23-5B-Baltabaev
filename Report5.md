# Day 5 Report — Module 8 Capstone

## 1) Student
- **Name:** Baltabaev_Dinmukhamed
- **Group:** IB23-5B
- **Token:** D1-IB-23-5b-03-0D9E
- **Repo:** https://github.com/DSmasher-git/devnet-day1-IB23-5B-Baltabaev

---

## 2) YANG (Lab 8.3.5)
- **pyang version:** pyang 2.7.1
- **Tree contains `+--rw interfaces`:** Yes
- **Tree contains `enabled? boolean`:** Yes

**Evidence files:**
- `artifacts/day5/yang/ietf-interfaces.yang`
- `artifacts/day5/yang/pyang_version.txt`
- `artifacts/day5/yang/pyang_tree.txt`

**pyang tree output:**
```text
module: ietf-interfaces
  +--rw interfaces
  |  +--rw interface* [name]
  |     +--rw name                        string
  |     +--rw description?                string
  |     +--rw type                        identityref
  |     +--rw enabled?                    boolean
  |     +--rw link-up-down-trap-enable?   enumeration {if-mib}?
  +--ro interfaces-state
     +--ro interface* [name]
        +--ro name               string
        +--ro type               identityref
        +--ro admin-status       enumeration {if-mib}?
        +--ro oper-status        enumeration
```

---

## 3) Webex (Lab 8.6.7)
- **Logged in as:** Vash the Stampede
- **Room title contains token_hash8:** Yes (DevNet-Day5-8b19095c)
- **Message text contains token_hash8:** Yes (Day5 capstone done! token_hash8=8b19095c)

**Evidence files:**
- `artifacts/day5/webex/me.json`
- `artifacts/day5/webex/rooms_list.json`
- `artifacts/day5/webex/room_create.json`
- `artifacts/day5/webex/message_post.json`
- `artifacts/day5/webex/messages_list.json`

---

## 4) Packet Tracer Controller REST (Activity 8.8.3)
- **External access check shows "empty ticket":** Yes
- **serviceTicket saved:** Yes (NC-146-fee1745eeb5642daab2d-nbi)
- **network-device response received:** Yes (9 devices)
- **hosts response received:** Yes (6 hosts)
- **PT internal script ran:** Yes

**Evidence files:**
- `artifacts/day5/pt/external_access_check.json`
- `artifacts/day5/pt/serviceTicket.txt`
- `artifacts/day5/pt/network_devices.json`
- `artifacts/day5/pt/hosts.json`
- `artifacts/day5/pt/postman_collection.json`
- `artifacts/day5/pt/postman_environment.json`
- `artifacts/day5/pt/pt_internal_output.txt`

---

## 5) Commands output
```text
$ python src/day5_summary_builder.py
Building Day 5 summary...
{
  "schema_version": "5.0",
  "student": {
    "token": "D1-IB-23-5b-03-0D9E",
    "token_hash8": "8b19095c",
    "name": "Baltabaev_Dinmukhamed",
    "group": "IB23-5B"
  },
  "yang": { "ok": true },
  "webex": { "ok": true },
  "pt": { "ok": true },
  "validation_passed": true
}

$ pytest -q tests/test_day5_module8.py
.............................
29 passed in 0.17s
```

---

## 6) Problems & fixes

### Problem 1:
- **Problem:** Packet Tracer версии 8.2.2 не имеет встроенного Network Controller GUI
- **Fix:** Использовал curl вместо Postman для получения serviceTicket и выполнения REST запросов
- **Proof:** `artifacts/day5/pt/serviceTicket.txt`, `network_devices.json`, `hosts.json`

### Problem 2:
- **Problem:** `python` команда не найдена в системе
- **Fix:** Активировал виртуальное окружение командой `source .venv/bin/activate`
- **Proof:** Все скрипты успешно запустились после активации venv
