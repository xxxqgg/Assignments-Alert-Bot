# Load configurations from file
import yaml

import yaml
import os
import time
import pytz

with open("../configurations.yaml", 'r') as stream:
    try:
        data = yaml.safe_load(stream)
        token = data.get('TelegramBot')[0].get('token')
        tz = data.get('TelegramBot')[0].get('time_zone')
        os.environ['TZ'] = tz
        if hasattr(time, 'tzset'):
            time.tzset()
        timezone = pytz.timezone(tz)
    except yaml.YAMLError as exc:
        print(exc)
