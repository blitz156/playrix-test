**Для запуска должны быть установлены:**

1. `docker` [https://docs.docker.com/install/linux/docker-ce/ubuntu/]
2. `docker-compose` [https://docs.docker.com/compose/install/]

**Запуск:**

1. ``docker-compose up``

**Запуск тестов:**

1. ``Заменить в docker-compose.yml выполняемую команду``
2. ``docker-compose up``

____________________________________


**Работа без docker**

**Запуск:**
1. ``Установить requirements.txt``
2.  ``python3 src/playrix_run.py``

**Запуск тестов:**
1. ``Установить requirements.txt``
2.  ``python3 src/playrix_test.py``

____________________________________


**P.S.**

Оценивая задание - прошу принять во внимание, что с pandas никогда до этого не работал.
Результат выполнения скрипта находится - `src/output/result.csv`