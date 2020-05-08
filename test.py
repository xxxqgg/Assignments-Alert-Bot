from telegram.ext import Updater, CommandHandler
import config


# Test code
def hello(update, context):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

def nb(update, context):
    update.message.reply_text("睿哥牛逼")

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

updater = Updater(config.token, use_context=True)

updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('nb', nb))
updater.dispatcher.add_handler(CommandHandler('start', start))

updater.start_polling()
updater.idle()