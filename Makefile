restart:
	sudo systemctl restart bot.service

start:
	sudo systemctl start bot.service

stop:
	sudo systemctl stop bot.service

status:
	sudo systemctl status bot.service

journal:
	journalctl -u bot.service

shell:
	poetry shell

dev:
	python3 bot/main.py

install:
	poetry install

dbcreate:
	python3 bot/createdb.py