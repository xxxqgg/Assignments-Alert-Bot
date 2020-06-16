from telegram.ext import Updater, CommandHandler, PicklePersistence
from telegram.ext import CallbackContext
import config
from Assignment import Assignment, Assignments
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


def get_assignments(assignments: Assignments):
    if assignments is None or len(assignments) == 0:
        return "目前没有作业 ;-)"
    message = "目前有{}项作业 \n".format(len(assignments))
    for assignment in assignments:
        message += str(assignment)
        message += "\n"
    return message


# Display all assignments
def all(update, context):
    assignments = context.chat_data.get(assignment_key)
    reply_message = get_assignments(assignments)
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


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


def daily_assignment_alert(context: CallbackContext):
    dp = context.dispatcher
    for chat_id, chat_data in dp.chat_data.items():
        print(chat_data)
        reply_message = "~每日作业提醒~\n"
        assignments = chat_data.get(assignment_key)
        reply_message += get_assignments(assignments)
        context.bot.send_message(chat_id=chat_id, text=reply_message)


# Add Something
def add(update, context):
    assignment = Assignment(context.args[0], parser.parse(" ".join(context.args[1:])))
    if assignment_key not in context.chat_data.keys():
        context.chat_data[assignment_key] = Assignments()
    context.chat_data.get(assignment_key).add(assignment)
    reply_message = "{}\nsuccessfully added.".format(str(assignment))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


def remove(update, context):
    id = int(context.args[0])
    if assignment_key not in context.chat_data.keys():
        # This should be an error because there is no assignments object for this user.
        raise KeyError("This conversation don't have a assignments object")

    assignments = context.chat_data.get(assignment_key)
    try:
        obj = assignments.remove(id)
    except KeyError:
        reply_message = "id: {} not found.".format(id)
        context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)
        return

    reply_message = "{}\nsuccessfully removed.".format(str(obj))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


def detail(update, context):
    id = int(context.args[0])
    if assignment_key not in context.chat_data.keys():
        # This should be an error because there is no assignments object for this user.
        raise KeyError("This conversation don't have a assignments object")

    assignments = context.chat_data.get(assignment_key)
    reply_message = assignments[id].detail_str
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


# Check the Assignment
def check(update, context):
    print("Check")


if __name__ == '__main__':
    persistence = PicklePersistence(filename='bot_data.dat')
    updater = Updater(config.token, use_context=True, persistence=persistence)

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

    updater.dispatcher.add_handler(
        CommandHandler(
            'check',
            check,
            pass_args=True
        )
    )
    updater.dispatcher.add_handler(
        CommandHandler(
            'remove',
            remove,
            pass_args=True
        )
    )
    updater.dispatcher.add_handler(
        CommandHandler(
            'detail',
            detail,
            pass_args=True
        )
    )
    job_queue = updater.job_queue
    # job_queue.run_repeating(daily_assignment_alert, interval=10, first=0)
    job_queue.run_daily(daily_assignment_alert,
                        time=parser.parse("8:00").time().replace(tzinfo=config.timezone),
                        name="daily alert")
    updater.start_polling()
    updater.idle()
