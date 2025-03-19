### Запуск проекта:
```
docker compose up --build
```
### Запуск композа с тестами и генерация файла покрытия:
```
docker compose -f docker-compose.test.yml up --build --abort-on-container-exit
```
### Опенапи схема:
```
http://localhost:18000/docs
```
### Отчет по coverage:
```
coverage/index.html
```
### Нюансы, которые намеренно не учитывал:
1) вместо селери/крона для отмены резервирования написал простой скрипт, запускается раз в минуту, отменяет необработанные за 5 минут резервирования
2) вместо логгера - принты
3) БЛ во вьюхах 
4) Вместо пайдантик моделей респонсы на JSONResponse чтобы сделать быстро и соответствовать схемам по ТЗ, в реальности сделал бы с пайдантиком для нормальной валидации
5) Добавил дополнительные статусы для резервирований чтобы добавить логику аппрува и отмены, стартовый статус - "created"
6) pyproject.toml и uv.lock вместо requirements.txt для менеджа и установки зависимостей
7) энвы захардкожены, в реальности использовал бы переменные окружения
8) для тестов и сервиса одна и та же БД