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