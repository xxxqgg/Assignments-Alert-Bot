# Load configurations from file
import yaml

import yaml

with open("configurations.yaml", 'r') as stream:
    try:
        data = yaml.safe_load(stream)
        token = data.get('TelegramBot')[0].get('token')

    except yaml.YAMLError as exc:
        print(exc)