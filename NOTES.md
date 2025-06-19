

### To Do




### Local Development
python3 manage.py runserver

python3 manage.py test

ruff check --fix
ruff format

python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py showmigrations
python3 manage.py sqlmigrate

python3 manage.py shell


### Therory
N + 1
onetone, foriegnkey - select_related()
manytomany, reverse foriegnkey - prefetch_related()


### Quick SetUp
виртуалку + установить зависимости
django-admin startproject src .
python3 manage.py startapp myapp
myapp in src/settings.py
postgre + env + settings
migrate
createsuperuser


### Production Development
debug
secret key
media
static (collect static)
.env
ALLOWED_HOSTS


### All Main Tasks

⚙️ Celery + Redis — для отправки почты, обработки очередей, фоновых задач

⏰ Celery Beat — периодические задачи

3. WebSockets / Real-time
🔌 Django Channels — чат, уведомления, онлайн-статусы

4. Тестирование
✅ pytest-django — расширенные тесты

🧪 Factory Boy — генерация тестовых данных

5. DevOps и деплой
🐳 Docker / Docker Compose — оборачивай проект, БД, Redis и Celery

🔁 CI/CD — GitHub Actions для автотестов и деплоя

6. Хранение файлов
🗂️ Amazon S3 / Yandex Object Storage — хранение фото/видео, через django-storages

7. Оптимизация и кеширование
⚡ Low-level caching (cache_page, cache.get_or_set)

🧠 Redis как кеш и брокер задач

🗂️ Select_related / Prefetch_related — оптимизация запросов

8. Работа с фронтом / API
📦 OpenAPI / Swagger / Redoc (drf-yasg, drf-spectacular)

🔍 Throttling, Filtering, Pagination — углубись в DRF

9. Разработка REST API + Frontend
🔄 Vue 3 / React — создай отдельный SPA-клиент к DRF API

📱 Postman / Insomnia — прокачай тестирование и документирование API

10. RBAC и ACL
🛡️ Roles / Permissions / Groups — разграничение доступа

⚙️ Custom Permissions / View-level permissions

seeder / faker
cors + react
analyze миой проект django + drf от tms