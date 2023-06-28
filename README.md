## Проект Foodgram


### Технологии:

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

### Когда проголодаетесь не знаете, что приготовить?
### А в моменты прибывания кухонным шефом не хочется забыть рецепт своего кулинарного шедевра? 
### Foodgram - продуктовый помощник с базой кулинарных рецептов, который станет вашим верным инструментом!
С ним вы можете:
- Создать рецепт с уже предустановленной базой ингридиентов;
- Прикрепить теги, для быстрого поиска;
- Подписаться на других кулинаров;
- Добавить рецепты в избранное;
- Добавить рецепты в корзину, с которой будет скачан PDF файл с ингредиентами ваших выбранных рецептов;


### Развернуть проект на удаленном сервере:

- Клонировать репозиторий:
```
https://github.com/we5h/foodgram-project-react.git
```

- Установить на сервере Docker, Docker Compose:

```
sudo apt install curl                                   # установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      # скачать скрипт для установки
sh get-docker.sh                                        # запуск скрипта
sudo apt-get install docker-compose-plugin              # последняя версия docker compose
```

- Скопировать на сервер файлы docker-compose.production.yml

- Для работы с GitHub Actions необходимо в репозитории в разделе Secrets > Actions создать переменные окружения:
```
SECRET_KEY              # секретный ключ Django проекта
DOCKER_PASSWORD         # пароль от Docker Hub
DOCKER_USERNAME         # логин Docker Hub
HOST                    # публичный IP сервера
USER                    # имя пользователя на сервере
PASSPHRASE              # *если ssh-ключ защищен паролем
SSH_KEY                 # приватный ssh-ключ
TELEGRAM_TO             # ID телеграм-аккаунта для посылки сообщения
TELEGRAM_TOKEN          # токен бота, посылающего сообщение

.env(на сервере)
DB_ENGINE               # django.db.backends.postgresql
DB_NAME                 # postgres
POSTGRES_USER           # postgres
POSTGRES_PASSWORD       # postgres
DB_HOST                 # db
DB_PORT                 # 5432 (порт по умолчанию)
SECRET_KEY='секретный ключ Django'
ALLOWED_HOSTS=*
DEBUG_VALUE=True
```

- Создать и запустить контейнеры Docker, выполнить команду на сервере
*(версии команд "docker compose" или "docker-compose" отличаются в зависимости от установленной версии Docker Compose):*
```
sudo docker compose up -d
```

После успешной сборки:

- Создать суперпользователя:
```
sudo docker compose exec backend python manage.py createsuperuser
```

- Наполнить базу данных содержимым из файла ingredients.csv:
```
sudo docker compose exec backend python manage.py importcsv
```

- Для остановки контейнеров Docker:
```
sudo docker compose down -v      # с их удалением
sudo docker compose stop         # без удаления
```

### После каждого обновления репозитория (push в ветку master) будет происходить:

1. Проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8)
2. Сборка и доставка докер-образов frontend и backend на Docker Hub
3. Разворачивание проекта на удаленном сервере
4. Отправка сообщения в Telegram в случае успеха

### Запуск проекта на локальной машине:

- Клонировать репозиторий:
```
https://github.com/we5h/foodgram-project-react.git
```

- В корне проекта создать .env и заполнить своими данными:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY='секретный ключ Django'
ALLOWED_HOSTS=*
DEBUG_VALUE=True

```

- Создать и запустить контейнеры Docker, последовательно выполнить команды по
созданию суперпользователя, как указано выше.
```
docker-compose -f docker-compose.yml up -d
```


- После запуска проект будут доступен по адресу: [http://127.0.0.1:9001/](http://127.0.0.1:9001/)


- Документация будет доступна по адресу: [http://127.0.0.1:9001/api/docs/](http://127.0.0.1:9001/api/docs/)

## Автор

- Дмитрий Грибков [@we5h](https://www.github.com/we5h)
