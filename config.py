# Load configurations from file
import yaml

import yaml
import os
import time

with open("configurations.yaml", 'r') as stream:
    try:
        data = yaml.safe_load(stream)
        token = data.get('TelegramBot')[0].get('token')
        time_zone = data.get('TelegramBot')[0].get('time_zone')
        os.environ['TZ'] = time_zone
        if hasattr(time, 'tzset'):
            time.tzset()
    except yaml.YAMLError as exc:
        print(exc)
