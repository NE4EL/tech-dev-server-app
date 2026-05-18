# KR5 — Task Management API (FastAPI)

REST API для управления задачами с WebSocket-чатом и авторизацией через заголовки.

## Структура проекта

```
app/
  main.py          # FastAPI app, WebSocket, health endpoint
  schemas.py       # Pydantic модели
  storage.py       # In-memory хранилище
  dependencies.py  # DI: авторизация, роли, хранилище
  routers/
    tasks.py       # CRUD задач
    users.py       # Профиль пользователя
    admin.py       # Статистика и удаление для админа
tests/
  conftest.py      # Фикстуры pytest
  test_tasks.py    # Задание 1: тесты API задач
  test_docker.py   # Задание 2: тест health endpoint
  test_websocket.py # Задание 3: тесты WebSocket
  test_advanced.py # Задание 4: тесты DI и роутеров
Dockerfile
docker-compose.yml
requirements.txt
```

## Установка и запуск

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API доступно на `http://localhost:8000`. Документация: `http://localhost:8000/docs`.

## Запуск тестов

```bash
pytest
```

## Docker

```bash
# Сборка и запуск
docker-compose up --build

# Только сборка
docker build -t kr5-api .

# Запуск контейнера
docker run -p 8000:8000 -e APP_ENV=docker kr5-api
```

## Аутентификация

Все эндпоинты требуют заголовок `X-User-Id: <int>`. Для admin-роутов дополнительно `X-User-Role: admin`.

## Эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| GET | /health | Проверка состояния |
| POST | /tasks | Создать задачу |
| GET | /tasks | Список задач (фильтры: status, min_priority) |
| GET | /tasks/{id} | Получить задачу |
| PATCH | /tasks/{id}/status | Обновить статус |
| DELETE | /tasks/{id} | Удалить задачу |
| GET | /users/me | Профиль текущего пользователя |
| GET | /users/{id} | Профиль пользователя |
| GET | /admin/stats | Статистика (только admin) |
| DELETE | /admin/tasks/{id} | Удалить любую задачу (только admin) |
| WS | /ws/rooms/{room_id}?username= | WebSocket чат |
| GET | /rooms/{room_id}/users | Активные пользователи комнаты |
