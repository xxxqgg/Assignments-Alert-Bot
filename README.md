# Assignments Alert Bot

[@AssignmentsAlertBot](https://telegram.me/AssignmentsAlertBot)

Based on [python-telegram-bot](https://python-telegram-bot.org/)

## Usage
To directly use the bot: follow [@AssignmentsAlertBot](https://telegram.me/AssignmentsAlertBot)

To run the bot on your own server, follow the following steps:
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
        token: 1262663214:AAFxqx4reBnm2uR3ZPUqotBZJ7HYR1Pxsdg
        time_zone: Asia/Shanghai
    ```
3. Install pip packages
    ```bash
    pip install -r requirements.txt
    ```
4. Run the bot
    ```bash
    python3 main.py
    ```