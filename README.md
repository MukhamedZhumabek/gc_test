
## Тестовое приложение Global Coffee Test
- Python3.10.4
- FastAPI
- SQLalchemy2
- Pytest
- Docker, Docker-Compose
---

 - Простой CRUD
 - 2 сущности **Product** и **Store**
 - **Store** one-to-many **Product**

---

## Как быстро поднять проект?

### 1. Склонировать репозиторий

https
```console
git clone https://github.com/MukhamedZhumabek/gc_test.git && cd gc_test
```
ssh
```console
git clone git@github.com:MukhamedZhumabek/gc_test.git && cd gc_test
```
### 2. Поднять docker-compose
 - app(fastapi)   :8000
 - db(postgresql) :5432
```console
docker-compose up -d
```

### 3. Прогнать тесты и убедиться что все работает
```console
docker-compose exec app python -m pytest -v
```

### 4. FastApi предостовляет swagger из коробки 
>[Потыкать API](http://127.0.0.1:8000/docs)
---
## Как поднять приложение не в контейнере а локально для разработки?

1. Опустить контейнеры

```console
docker-compose down
```
2. В файле `settings.py` заменить `.env.postgres` на `.env.postgres.local`


3. Поднять базу данных
```console
docker-compose -f docker-compose.local.yml up -d
```

Что бы не париться с запуском проекта в пайчарме можно просто добавить в файл `main.py`
```python
if __name__ == '__main__':
    uvicorn.run(app=gc_test_app)
```
---


# API

### если проект поднят, то удобнее смотреть в [OpenAPI](http://127.0.0.1:8000/docs)

## Аутентификация и Aвторизация

Все запросы к  API требуют включения заголовка `auth-token`.

Сейчас за отсутсвием остальной инфраструктуры, захардкожен токен `secret`

Пользователь с токеном `secret` получает авторизацию на полный API

```json
{'auth-token': 'secret'}
```

## API для магазинов

### Получить магазин по ID

- **URL**: `/api/v1/store/{store_id}`
- **Метод**: `GET`
- **Описание**: Получить магазин по его внешнему ID.
- **Параметры**:
  - `store_id` (путь): Целое число - ID магазина
- **Заголовки запроса**:
  - `auth-token`: Строка - Аутентификационный токен
- **Ответы**:
  - `200 OK`: Успешный ответ. Возвращает детали магазина.
  - `404 Ошибка запроса`: Магазин не найден
  - `422 Ошибка валидации`: Если есть ошибка в параметрах запроса.

### Создать новый магазин

- **URL**: `/api/v1/store/`
- **Метод**: `POST`
- **Описание**: Создать новый магазин.
- **Заголовки запроса**:
  - `auth-token`: Строка - Аутентификационный токен
- **Тело запроса**:
  - JSON-объект с следующими свойствами:
    - `name`: Строка - Название магазина
    - `description`: Строка (опционально) - Описание магазина
    - `address`: Строка (опционально) - Адрес магазина
- **Ответы**:
  - `200 OK`: Успешный ответ. Возвращает детали созданного магазина.
  - `400 Неправильные данные`: Если есть ошибка в логике запроса.
  - `422 Ошибка валидации`: Если есть ошибка в параметрах запроса.

## APi для Product

### Получить продукт по внешнему ID

- **URL**: `/api/v1/product/{external_id}`
- **Метод**: `GET`
- **Описание**: Получить продукт по его внешнему ID.
- **Параметры**:
  - `external_id` (путь): Строка - Внешний ID продукта
- **Заголовки запроса**:
  - `auth-token`: Строка - Аутентификационный токен
- **Ответы**:
  - `200 OK`: Успешный ответ. Возвращает детали продукта.
  - `404 Ошибка запроса`: Продукт не найден
  - `422 Ошибка валидации`: Если есть ошибка в параметрах запроса.

### Создать новый продукт

- **URL**: `/api/v1/product/`
- **Метод**: `POST`
- **Описание**: Создать новый продукт.
- **Заголовки запроса**:
  - `auth-token`: Строка - Аутентификационный токен
- **Тело запроса**:
  - JSON-объект с следующими свойствами:
    - `external_id`: Строка - Внешний ID продукта
    - `name`: Строка - Название продукта
    - `description`: Строка (опционально) - Описание продукта
    - `store_id`: Целое число - ID магазина, к которому принадлежит продукт
- **Ответы**:
  - `200 OK`: Успешный ответ. Возвращает детали созданного продукта.
  - `400 Неправильные данные`: Если есть ошибка в логике запроса.
  - `422 Ошибка валидации`: Если есть ошибка в параметрах запроса.

### Обновить продукт

- **URL**: `/api/v1/product/{external_id}/{store_id}`
- **Метод**: `PUT`
- **Описание**: Обновить продукт по его внешнему ID и ID магазина.
- **Заголовки запроса**:
  - `auth-token`: Строка - Аутентификационный токен
- **Тело запроса**:
  - JSON-объект с следующими свойствами:
    - `name`: Строка - Название продукта
    - `description`: Строка (опционально) - Описание продукта
- **Ответы**:
  - `200 OK`: Успешный ответ. Возвращает детали обновленного продукта.
  - `400 Неправильные данные`: Если есть ошибка в логике запроса.
  - `422 Ошибка валидации`: Если есть ошибка в параметрах запроса.

### Удалить продукт

- **URL**: `/api/v1/product/{external_id}/{store_id}`
- **Метод**: `DELETE`
- **Описание**: Удалить продукт по его внешнему ID и ID магазина.
- **Параметры**:
  - `external_id` (путь): Строка - Внешний ID продукта
  - `store_id` (путь): Целое число - ID магазина, к которому принадлежит продукт
- **Заголовки запроса**:
  - `auth-token`: Строка - Аутентификационный токен
- **Ответы**:
  - `200 OK`: Успешный ответ. Возвращает детали удаленного продукта.
  - `404 Ошибка запроса`: Продукт не найден
  - `422 Ошибка валидации`: Если есть ошибка в параметрах запроса.