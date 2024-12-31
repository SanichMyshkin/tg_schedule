# Telegram bot for mailing schedules and weather

You can try this [demo](https://t.me/Schedule_ICTMS_BOT) if you want to understand how this bot works 

To install the project and run the project, you need to copy the repository using the command:
```commandline
git clone git@github.com:SanichMyshkin/tg_schedule.git
cd tg_schedule
```



### Next, make sure that you have the [poetry](https://python-poetry.org) package manager installed

Environment variables are required for correct operation
Create a file [.env](https://dev.to/edgar_montano/how-to-setup-env-in-python-4a83) at the root of the project

It is necessary to fill in .env with the following contents
```commandline
TOKEN = 'your telegram bot token'
CHAT_ID = 'id of the chat to which you want to send the schedule by time'
WEATHER_API_KEY = "your api key for weather"
```


before installing dependencies, you need to run the virtual environment using the command

```commandline
make shell
```

In order to create the service, which will support this bot in active state we need to execute following commands

```
cd /etc/systemd/system
touch bot.service
```
Fill file `bot.service` with following data

```
[Unit]
Description=Telegram bot schedule

[Service]
User=root
WorkingDirectory=/home/tg_schedule
ExecStart=/home/tg_schedule/.venv/bin/python bot/main.py

Restart=always
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

In field `WorkingDirectory` - write path to this project

`ExecStart` - write path to Python interpritator and write path to executable file (by default in project `bot/main.py`) 

It remains only to install the necessary packages, and run it using the following commands

In order to create database you need to execute the command

```
make dbcreate
```

You need to fill database with your data. You can look up the structure of the database schemas in the `createdb.py` file.


```commandline
make install
make start
```


Also, if you want to stop or restart the bot, use the following commands
```commandline
make stop
make restart
```
