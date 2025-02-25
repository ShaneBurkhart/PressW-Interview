.PHONY: run

C := backend

all: run

boot:
	touch .env
	$(MAKE) build
	$(MAKE) npm
	$(MAKE) restart

build:
	docker compose build

run:
	docker compose up

clean:
	docker compose down

restart:
	$(MAKE) clean
	$(MAKE) run

c:
	docker compose run --rm $(C) bash

npm:
	docker compose run --rm frontend npm install

pip:
	docker compose run --rm backend pip install -r requirements.txt

install:
	$(MAKE) pip
	$(MAKE) npm
