from telegram.ext import Updater, CommandHandler
import config
from Assignment import Assignment
from datetime import datetime, time, timezone
from dateutil import parser

assignment_key = "assignments"
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
    if assignment_key not in context.chat_data.keys() or len(context.chat_data.get(assignment_key)) <= 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="目前没有作业 ;-)")
        return
    reply_message = "目前有{}项作业 \n".format(len(context.chat_data.get(assignment_key)))
    assignments = context.chat_data.get(assignment_key)

    for assignment in context.chat_data.get(assignment_key):
        reply_message += str(assignment)
        reply_message += "\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)


# Daily Alarm
def update_repeatment(update, context):
    if 'job' in context.chat_data:
        old_job = context.chat_data['job']
        old_job.schedule_removal()
    new_job = context.job_queue.run_daily(
        callback=all,
        time=time(14, 33, 0)
    )
    # print("add a new job")
    context.chat_data['jpb'] = new_job



# Add Something
def add(update, context):
    # title = context.args[0]
    # due_time =
    assignment = Assignment(context.args[0], parser.parse(" ".join(context.args[1:])))
    if assignment_key in context.chat_data.keys():
        context.chat_data.get(assignment_key).append(assignment)
    else:
        context.chat_data[assignment_key] = [assignment]

    # update_repeatment(update, context)

    # for arg in context.args:
    #     print(arg)


if __name__ == '__main__':
    updater = Updater(config.token, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(
        CommandHandler(
            'today',
            today,
            pass_args=True
        )
    )

    updater.dispatcher.add_handler(
        CommandHandler(
            'add',
            add,
            pass_args=True
        )
    )

    updater.dispatcher.add_handler(
        CommandHandler(
            'all',
            all,
            pass_args=True
        )
    )
    updater.start_polling()
    updater.idle()
