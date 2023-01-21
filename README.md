# Проектная работа 6 спринта

[Ссылка на репозиторий](https://github.com/sevrn73/Auth_sprint_1)

Участники @sevrn73, @rachet2012

## Запуск проекта

1. Создаем файл .env на основе .env_example (копируем и редактируем)
2. Запускаем docker-compose

```
docker-compose up
```

- Все миграции пройдут автоматически

3. Создаем суперпользователя. Нужно зайти в контейнер с Flask и запустить консольную команду (не забудьте указать свой логин и пароль)

```
docker-compose exec auth_api bash

python3 -m flask create_admin_role yourLogin yourPassword
```

3. Запускаем тесты

```
docker-compose exec auth_api pytest
```

## Доступные сервисы

- [OpenAPI](http://localhost/docs/)

## Представленные enpoints:

Управление авторизацией:

- Авторизация пользователя: **POST /api/v1/login**
- Создание пользователя: **POST /api/v1/sign_up**
- Подтверждение валидности access tokena: - **POST /api/v1/access**
- Выход пользователя (помещает переданные токены в блоклист): **DELETE /api/v1/logout**
- Для валидного refresh-токена возвращает пару токенов access+refresh: **GET /api/v1/refresh**
- Изменение логина пользователя: - **POST /api/v1/change_login**
- Изменение пароля пользователя: - **POST /api/v1/change_password**
- Получение истории авторизации пользователя: - **GET /api/v1/login_history**

Управление ролями:

- Получение списка ролей: **GET /api/v1/roles_list**
- Создание роли: **POST /api/v1/create_role**
- Удаление роли: **DELETE /api/v1/delete_role**
- Изменение роли: **PUT /api/v1/change_role**

Управление пользователями:

- Добавление роли пользователю: **POST /api/v1/assign_role**
- Удаление роли у пользователя: **DELETE /api/v1/detach_role**
