## Работа с миграциями Alembic

Инициализация Alembic
```bash
alembic init alembic
```

Создать пустую миграцию
```bash
alembic revision --autogenerate -m "create initial tables"
```

Установить миграцию как текущую без реальных изменений в базе данных.<br>
На случай если таблицы в базе уже есть, но добавляли мы их вручную без миграций. 
```bash
alembic stamp head
```

Обновить до последней миграции (создает и меняет таблицы).
```bash
alembic upgrade head
```

Показать SQL без применения миграции.
```bash
alembic upgrade head --sql
```

Показать текущую миграцию.
```bash
alembic current
```

Показать историю миграций.
```bash
alembic history
```
