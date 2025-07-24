NETWORK_NAME=undergroundvpn

up-main:
	docker-compose -f docker-compose.yml up -d --build

up-cell:
	docker-compose -f vpn_cell_service/docker-compose.yml up -d --build

up: up-main up-cell

down-main:
	docker-compose -f docker-compose.yml down

down-cell:
	docker-compose -f vpn_cell_service/docker-compose.yml down

down: down-cell down-main

migrations:
	docker-compose -f docker-compose.yml run vpn-gate alembic revision --autogenerate

migrate:
	docker-compose -f docker-compose.yml run vpn-gate alembic upgrade head
	