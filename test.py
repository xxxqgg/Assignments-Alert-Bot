from telegram.ext import Updater, CommandHandler
import config

# Examples

# Reply a message, will reply (which will notify) the person who sends the command.
def hello(update, context):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name)
    )

# Send a message, will NOT reply the person who sends the command.
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

# Handling arguments. Need to set 'pass_args = True' in CommandHandler()
# TODO: Display assignments which due today
def today(update, context):
    arg = context.args[0]
    print("Here " + arg)

# Display all assignments
def all(update, context):
    print("all")


# Add Something
def add(update, context):
    for arg in context.args:
        print(arg)



updater = Updater(config.token, use_context=True)

updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(
    CommandHandler(
        'today',
        today,
        pass_args = True
    )
)

updater.dispatcher.add_handler(
    CommandHandler(
        'add',
        add,
        pass_args = True
    )
)



updater.start_polling()
updater.idle()