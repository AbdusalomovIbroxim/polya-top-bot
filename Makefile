# Используем docker compose (предпочтительно над docker-compose)
COMPOSE = docker compose

# Определяем цели как "чистые" (не связанные с файлами)
.PHONY: build up up-d logs down shell-buyursin shell-polya

# --------------------------
# ОСНОВНЫЕ ОПЕРАЦИИ СТЕКА
# --------------------------

# Сборка образов для всех сервисов
build:
	$(COMPOSE) build

# Запуск всех сервисов в интерактивном режиме (для отладки)
up: build
	$(COMPOSE) up

# Запуск всех сервисов в фоновом режиме
up-d: build
	$(COMPOSE) up -d

# Просмотр логов всех сервисов
logs:
	$(COMPOSE) logs -f

# Остановка и удаление контейнеров (том с данными PostgreSQL сохраняется)
down:
	$(COMPOSE) down