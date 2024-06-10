# TestTaskDjango

## Описание

Этот проект представляет собой систему управления задачами, где задачи могут создаваться и управляться как сотрудниками (employees), так и клиентами (customers). Проект предоставляет API для управления задачами с использованием Django и Django REST Framework. В проекте также используется Swagger для документирования API.

## Требования

- Docker
- Docker Compose

## Установка и запуск

### Шаг 1: Клонируйте репозиторий

```bash
git clone https://github.com/MikhailPrizba/TestovoePythonDev.git
cd TestTaskDjango
```

### Шаг 2: Создайте файл окружения

Создайте файл `.env` в корневом каталоге проекта по примеру `.env.example`.

Пример `.env` файла:

```
DJANGO_SECRET_KEY=your_secret_key
POSTGRES_DB=your_db
POSTGRES_USER=your_user
POSTGRES_ENGINE = 'django.db.backends.postgresql_psycopg2'
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
ALLOWED_HOSTS = 'localhost'
```

### Шаг 3: Настройка прав

Убедитесь, что файл `entrypoint/project.sh` имеет права на выполнение:

```bash
chmod +x entrypoint/project.sh
```

### Шаг 4: Запуск Docker Compose

Запустите проект с помощью Docker Compose:

```bash
sudo docker compose up -d
```

### Шаг 5: Создание суперпользователя

Для создания суперпользователя выполните команду:

```bash
sudo docker compose exec web python manage.py createsuperuser
```

### Шаг 6: Добавление сотрудника

Перейдите в админку по адресу `http://localhost:8000/admin` и добавьте сотрудника (employee).

## Документация API

Swagger документация доступна по адресу: `http://localhost:8000/api/v1/swagger`

## Структура проекта

- `tasks/` - приложение для управления задачами.
- `users/` - приложение для управления пользователями.
- `project/` - основные настройки проекта.
- `entrypoint/` - скрипты для настройки контейнеров.

## Тестирование

Для запуска тестов используйте команду:

```bash
sudo docker compose exec web pytest
```

## Фото

Передаем в формате

'R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='
