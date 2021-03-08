# Assignments Alert Bot
A bot used for grouping assignments and TODOs.

[@AssignmentsAlertBot](https://telegram.me/AssignmentsAlertBot)

Based on [python-telegram-bot](https://python-telegram-bot.org/)

## Usage
- /all: Display all the assignments.
- /add: Add an assignment. Arguments: /add [AssignmentName] [Date and time]. 
    There are certain limitations to this command:
    1. There MUST BE NO SPACE in AssignmentName
    2. The date must be in format like MM-dd
    3. The time must be in format like hh:mm:ss
- /remove: Remove an assignment. Arguments: /remove [assignment_id]
- /stop: Stop the bot from sending daily alerts. There must be no assignments left to use this command.

## Usage
Feel free to use the bot directly: follow [@AssignmentsAlertBot](https://telegram.me/AssignmentsAlertBot)

### Deployment
You can run the bot on your own server. There are two methods doing this.

#### Deploy via Docker
1. clone the repository on the server
    ```bash
    git clone https://github.com/xxxqgg/Assignments-Alert-Bot.git
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
3. [Install Docker](https://docs.docker.com/engine/install/) on your server if not previously  installed.
4. Run via docker:
    ```bash
    docker-compose up -d
    ```
    
#### Deploy directly
1. clone the repository on the server
    ```bash
    git clone https://github.com/xxxqgg/Assignments-Alert-Bot.git
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
