import i18n

i18n.config.set("file_format", 'yaml')

i18n.load_path.append('./translations')
if __name__ == '__main__':
    print(i18n.t('assignment.daily_alert', locale='zh'))