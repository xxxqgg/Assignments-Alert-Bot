# Assignments Alert Bot
A bot used for grouping assignments and TODOs.

[@AssignmentsAlertBot](https://telegram.me/AssignmentsAlertBot)

Based on [python-telegram-bot](https://python-telegram-bot.org/)

## Usage
Feel free to use the bot directly: follow [@AssignmentsAlertBot](https://telegram.me/AssignmentsAlertBot)

Or you can run the bot on your own server:
1. clone the repository on the server
    ```bash
    git clone git@github.com:xxxqgg/Assignments-Alert-Bot.git
    ```
2. Make a copy of ```configurations-template.yaml``` and name it 
to ```configurations.yaml```. Change the configurations accordingly.
For example, a configuration would look like:
    ```yaml
    TelegramBot:
      - name: AssignmentBot
        token: 1231231231:AAFxqx4reBnm2uR3ZPUqotBZJ7HYR1Pxsdg
        time_zone: Asia/Shanghai
    ```
3. Install pip packages
    ```bash
    pip install -r requirements.txt
    ```
4. Run the bot
    ```bash
    python3 src/main.py
    ```