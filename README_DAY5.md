# Day 5 — Пошаговая инструкция

## Что понадобится
- DEVASC VM (для Packet Tracer части)
- Webex аккаунт + Personal Access Token
- Python 3, pip, wget

---

## Шаг 0 — Копируем файлы в репозиторий

Скопируй папку `day5/` в корень своего репозитория. Структура должна быть:

```
devnet-day1-Baltabaev/
├── src/
│   ├── day5_module8.py          ← новый
│   └── day5_summary_builder.py  ← новый
├── schemas/
│   └── day5_summary.schema.json ← новый
├── tests/
│   └── test_day5_module8.py     ← новый
├── scripts/
│   ├── setup_yang.sh            ← новый
│   └── pt_internal_script.py   ← новый
├── artifacts/
│   └── day5/
│       └── pt/
│           ├── postman_collection.json   ← новый
│           └── postman_environment.json  ← новый
├── .env.example                 ← обновлённый
└── Day5_report.md               ← новый
```

---

## Шаг 1 — Настройка .env

```bash
cp .env.example .env
# Открой .env и заполни:
# STUDENT_TOKEN=...   (из прошлых дней)
# STUDENT_NAME=Baltabaev
# STUDENT_GROUP=...
# WEBEX_TOKEN=...     (получим на следующем шаге)
```

---

## Шаг 2 — Получение Webex токена (Lab 8.6.7, часть 1)

1. Открой https://developer.webex.com
2. Войди своим аккаунтом Cisco (или создай)
3. Нажми на своё фото → **Copy Personal Access Token**
4. Вставь в `.env` как `WEBEX_TOKEN=...`

> ⚠️ Токен живёт ~12 часов. Делай Webex часть сразу!

---

## Шаг 3 — YANG (Lab 8.3.5)

```bash
# Из корня репозитория:
chmod +x scripts/setup_yang.sh
./scripts/setup_yang.sh
```

Скрипт:
- установит/обновит `pyang`
- скачает `ietf-interfaces.yang`
- запустит `pyang -f tree`
- сохранит все файлы в `artifacts/day5/yang/`

**Проверь результат:**
```bash
cat artifacts/day5/yang/pyang_tree.txt | head -20
# Должно быть: +--rw interfaces
```

---

## Шаг 4 — Webex Python (Lab 8.6.7)

```bash
# Загрузи переменные из .env:
export $(grep -v '^#' .env | xargs)

# Установи requests если нет:
pip install requests python-dotenv --quiet

# Запусти:
python src/day5_module8.py webex
```

Проверь что появились файлы:
```bash
ls artifacts/day5/webex/
# me.json  rooms_list.json  room_create.json  message_post.json  messages_list.json
```

---

## Шаг 5 — Packet Tracer (Activity 8.8.3) — на DEVASC VM

### 5.1 Включи External Access в Packet Tracer
1. Открой Packet Tracer
2. Extensions → PT Network Controller → Settings
3. Включи External Access, запомни порт (обычно 58000)

### 5.2 Проверь доступ без токена
```bash
curl -s http://localhost:58000/api/v1/host > artifacts/day5/pt/external_access_check.json
cat artifacts/day5/pt/external_access_check.json
# Должно быть: "Ticket-based authorization: empty ticket."
```

### 5.3 Получи serviceTicket в Postman
1. Импортируй в Postman: `artifacts/day5/pt/postman_collection.json`
2. Импортируй environment: `artifacts/day5/pt/postman_environment.json`
3. Выбери environment "PT Controller — Day5"
4. Запусти запрос "1. Get Service Ticket"
5. Скопируй `serviceTicket` из ответа

```bash
# Сохрани ticket в файл:
echo "ТВОЙ_TICKET_ЗДЕСЬ" > artifacts/day5/pt/serviceTicket.txt
```

### 5.4 Выполни GET запросы с токеном
Обнови `serviceTicket` в Postman Environment, затем запусти:
- "2. GET Network Devices" → сохрани ответ как `network_devices.json`
- "3. GET Hosts" → сохрани ответ как `hosts.json`

```bash
# Или через curl (замени TICKET на свой):
TICKET=$(cat artifacts/day5/pt/serviceTicket.txt)
curl -H "X-Auth-Token: $TICKET" http://localhost:58000/api/v1/network-device \
  > artifacts/day5/pt/network_devices.json
curl -H "X-Auth-Token: $TICKET" http://localhost:58000/api/v1/host \
  > artifacts/day5/pt/hosts.json
```

### 5.5 PT Internal Python (Part 6)
1. В Packet Tracer открой Python проект
2. Скопируй содержимое `scripts/pt_internal_script.py`
3. Запусти, скопируй вывод консоли
4. Сохрани в `artifacts/day5/pt/pt_internal_output.txt`

---

## Шаг 6 — Сборка summary.json

```bash
export $(grep -v '^#' .env | xargs)
python src/day5_summary_builder.py
```

---

## Шаг 7 — Запуск тестов

```bash
pip install pytest jsonschema --quiet
pytest -q tests/test_day5_module8.py
```

Все тесты должны пройти ✓

---

## Шаг 8 — Коммит

```bash
git add artifacts/day5/ src/day5_*.py schemas/day5_*.json tests/test_day5_*.py Day5_report.md
git commit -m "Day 5: YANG + Webex + PT Controller REST API"
git push
```

---

## Структура итоговых файлов

```
artifacts/day5/
├── yang/
│   ├── ietf-interfaces.yang
│   ├── pyang_version.txt
│   └── pyang_tree.txt
├── webex/
│   ├── me.json
│   ├── rooms_list.json
│   ├── room_create.json       ← title содержит token_hash8
│   ├── message_post.json      ← text содержит token_hash8
│   └── messages_list.json
├── pt/
│   ├── external_access_check.json  ← содержит "empty ticket"
│   ├── serviceTicket.txt
│   ├── network_devices.json
│   ├── hosts.json
│   ├── postman_collection.json
│   ├── postman_environment.json
│   └── pt_internal_output.txt
└── summary.json
```
