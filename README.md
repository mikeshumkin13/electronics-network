# Electronics Network — Django + DRF + Postgres

Иерархическая сеть по продаже электроники (завод → розница → ИП).
Админка, API (CRUD), фильтрация по стране, запрет изменять долг через API.
Доступ к API — только активным сотрудникам.

## Стек
- Python 3.12 (подходят 3.9+)
- Django 4.2
- DRF 3.15
- PostgreSQL 14 (подойдёт 10+)
- django-filter
- Poetry (или `pip`)

## Быстрый старт (локально)

# 0) клонировать
git clone <repo-url> && cd electronics-network

# 1) окружение
cp .env.example .env

# 2) поднять Postgres (порт 5432)
docker compose up -d

# 3) зависимости
poetry install          # или: pip install -r requirements.txt (если используете pip)

# 4) миграции и суперпользователь
poetry run python manage.py migrate
poetry run python manage.py createsuperuser

# 5) запуск
poetry run python manage.py runserver

 Админка: http://127.0.0.1:8000/admin/

API root: http://127.0.0.1:8000/api/

# Модели
Product

name, model, release_date

NetworkNode

контакты: email, country, city, street, house

supplier — FK на NetworkNode (самоссылка)

products — M2M к Product

debt — Decimal(12,2), задолженность перед поставщиком

created_at — дата создания

level — уровень в иерархии (0 у корня), вычисляется автоматически от supplier

Админка

список Network nodes с колонками: level, city, country, supplier, debt

фильтры: по city, country, level

ссылка на поставщика (кликабельная)

action: «обнулить задолженность» (массово ставит debt=0.00)

API (DRF)
Доступ

Только аутентифицированные пользователи и с флагом is_staff=True и is_active=True.

Аутентификация: Session или Basic.

Эндпоинты

GET/POST /api/products/

GET/PATCH/DELETE /api/products/{id}/

GET/POST /api/network-nodes/?country=<ISO или строка>

GET/PATCH/DELETE /api/network-nodes/{id}/

Важные правила

Поле debt недоступно для изменения через API (read-only).

Продукты для узла передаём через product_ids (список ID), а читаем красивым вложенным products.


# Примеры`:

## Авторизация Basic (пример)
curl -u admin:password http://127.0.0.1:8000/api/products/

## Создать продукт
curl -u admin:password -H "Content-Type: application/json" \
 -d '{"name":"Phone","model":"X100","release_date":"2024-01-15"}' \
 http://127.0.0.1:8000/api/products/

## Создать узел сети (привязка к продуктам по id)
curl -u admin:password -H "Content-Type: application/json" \
 -d '{"name":"Розничная сеть","email":"r@ex.com","country":"RU","city":"СПб","street":"Невский","house":"1","product_ids":[1,2]}' \
 http://127.0.0.1:8000/api/network-nodes/

## Фильтрация по стране
curl -u admin:password "http://127.0.0.1:8000/api/network-nodes/?country=RU"

## Попытка изменить debt (не сработает — поле read-only)
curl -u admin:password -X PATCH -H "Content-Type: application/json" \
 -d '{"debt":"999.99"}' \
 http://127.0.0.1:8000/api/network-nodes/1/


