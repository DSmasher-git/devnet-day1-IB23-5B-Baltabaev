Day 4 Report — Labs 6–7 (Docker + Jenkins + Security + Ansible)
1) Student
* **Токен:** D1-IB-23-5b-03-0D9E
* **Имя:** Baltabaev_Dinmukhamed
* **Группа:** IB23-5B

Repo: https://github.com/DSmasher-git/devnet-day1-IB23-5B-Baltabaev

2) Evidence checklist (files exist)
Docker (6.2.7)
artifacts/day4/docker/sampleapp_curl.txt: Exists

artifacts/day4/docker/sampleapp_token_proof.txt: Exists

artifacts/day4/docker/sampleapp_docker_ps.txt: Exists

artifacts/day4/docker/sampleapp_build_log.txt: Exists

Jenkins (6.3.6)
artifacts/day4/jenkins/jenkins_docker_ps.txt: Exists

artifacts/day4/jenkins/buildapp_console.txt: Exists

artifacts/day4/jenkins/testapp_console.txt: Exists

artifacts/day4/jenkins/pipeline_script.groovy: Exists

artifacts/day4/jenkins/pipeline_console.txt: Exists

artifacts/day4/jenkins/jenkins_url.txt: Exists

Ansible (7.4.8)
artifacts/day4/ansible/ansible_ping.txt: Exists

artifacts/day4/ansible/ansible_hello.txt: Exists

artifacts/day4/ansible/ansible_playbook_install.txt: Exists

artifacts/day4/ansible/ports_conf_after.txt: Exists

artifacts/day4/ansible/curl_apache_8081.txt: Exists

Security (6.5.10)
artifacts/day4/security/signup_v1.txt: Exists

artifacts/day4/security/login_v1.txt: Exists

artifacts/day4/security/signup_v2.txt: Exists

artifacts/day4/security/login_v2.txt: Exists

artifacts/day4/security/db_tables.txt: Exists

artifacts/day4/security/db_user_hash_sample.txt: Exists

3) Commands output
Plaintext
$ pytest -v tests/test_day4_labs.py
=============================== test session starts ===============================
platform linux -- Python 3.8.2, pytest-8.3.5
tests/test_day4_labs.py::test_day4_summary_and_required_evidence PASSED      [100%]
================================ 1 passed in 0.25s ================================
4) Short reflection
Сегодняшний день охватил ключевые инструменты DevOps: контейнеризацию, CI/CD и автоматизацию конфигураций. Самым сложным было обеспечить корректную передачу и проверку уникального TOKEN_HASH8 внутри Docker-контейнера, так как малейшее несовпадение в символах приводило к провалу тестов. В части Security было полезно на практике увидеть разницу между хранением паролей в открытом виде и хешированным SHA-256 в базе данных SQLite.

5) Problems & fixes
Problem: Ошибка Connection refused при попытке выполнить curl запросы к Flask-серверу в Lab 6.5.10.
Fix: Проблема была вызвана тем, что сервер не был запущен. Решил проблему запуском скрипта security_app.py в отдельном терминале перед выполнением curl команд.
Proof: Файлы signup_v1.txt и db_user_hash_sample.txt успешно созданы и содержат корректные данные.