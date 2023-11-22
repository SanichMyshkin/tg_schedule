restart:
	sudo systemctl restart bot.service

start:
	sudo systemctl start bot.service

stop:
	sudo systemctl stop bot.service

shell:
	poetry shell

dev:
	python3 bot/main.py

install:
	poetry install

test:
	poetry run pytest

test-cov:
	 pytest --cov=bot

pu:
	git add .
	git commit -m "something fix"
	git push