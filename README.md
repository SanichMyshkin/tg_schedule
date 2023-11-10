# Telegram bot for mailing schedules and weather

To install the project and run the project, you need to copy the repository using the command:
```commandline
    git clone git@github.com:SanichMyshkin/tg_schedule.git
```
### Next, make sure that you have the poetry package manager installed
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

It remains only to install the necessary packages, and run it using the following commands

```commandline
make install
make satrt
```


Also, if you want to stop or restart the bot, use the following commands
```commandline
make stop
make restart
```


## Notes
You also need to create a database with your schedule for English with an existing one, as well as to fill the bot on the VPS service for full-fledged work, good luck!