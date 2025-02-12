# KOMTEK_test
Сервис терминологии, который хранит коды данных и их контекст (база данных справочников).

Документация к API доступна [здесь](http://127.0.0.1:8000/swagger/)

В документации описаны возможные запросы к API и структура ожидаемых ответов.

### Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone https://github.com/Maru-coder/KOMTEK_test.git
```

```bash
cd terminology_service
```

Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
source venv/Scripts/activate
```

```bash
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

Выполнить миграции:

```bash
python manage.py migrate
```

Запустить проект:

```bash
python manage.py runserver
```

### 
Ежова Марина
