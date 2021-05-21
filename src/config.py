# Load configurations from file
import yaml
import os
import time
import pytz
import i18n

i18n.config.set("file_format", 'yaml')
with open("configurations.yaml", 'r') as stream:
    try:
        data = yaml.safe_load(stream)
        token = data.get('TelegramBot')[0].get('token')
        tz = data.get('TelegramBot')[0].get('time_zone')
        os.environ['TZ'] = tz
        if hasattr(time, 'tzset'):
            time.tzset()
        timezone = pytz.timezone(tz)
        db_user = data.get('Database')[0].get('db_user')
        db_password = data.get('Database')[0].get('db_password')
        db_name = data.get('Database')[0].get('db_name')
        db_url = data.get('Database')[0].get('db_url')

    except yaml.YAMLError as exc:
        print(exc)
