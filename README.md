# kvartirka-comment-service

## Как развернуть проект из файла docker-compose(используется gunicorn и postgresql):
1. Склонировать проект, настроить .env файл:
    ```
    git clone git@github.com:pakodev28/kvartirka-comment-service.git
    ```
    ```
    cd kvartirka-comment-service
    ```
    ```
    copy .env.example .env
    ```
2. для запуска контейнеров:
    ```
    docker-compose up -d
    ```
3. Далее выполните следующие команды:
    ```
    docker-compose exec web python manage.py migrate --noinput
    ```
    ```
    docker-compose exec web python manage.py collectstatic --noinput
    ```
4. Можете загрузить датасет комментариев в БД:
    ```
    docker-compose exec web python manage.py loaddata data.json
    ```


## Как развернуть проект иcпользуя стандартные sqlite и стандартный development server:
1. Склонировать проект, перейти в директорию с проектом, создать и открыть виртуальное окружение:
    ```
    git clone git@github.com:pakodev28/kvartirka-comment-service.git
    ```
    ```
    cd kvartirka-comment-service
    ```
    ```
    python3 -m venv venv
    ```
    ```
    source venv/bin/activate
    ```
2. Далее выполните следующие команды:
    ```
    python3 manage.py migrate
    ```
    ```
    python3 manage.py loaddata data.json
    ```
    ```
    python3 manage.py runserver
    ```


## Доступные эндпоинты можно получит по адрессу:
http://127.0.0.1:8000/swagger/