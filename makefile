NETWORK_NAME=undergroundvpn

up:
	docker-compose -f docker-compose.yml up -d --build

down:
	docker-compose -f docker-compose.yml down

migrations:
	docker-compose -f docker-compose.yml run vpn-gate alembic revision --autogenerate

migrate:
	docker-compose -f docker-compose.yml run vpn-gate alembic upgrade head
	