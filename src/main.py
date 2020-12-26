from telegram.ext import Updater, CommandHandler, PicklePersistence
from telegram.ext import CallbackContext
from telegram.update import Update
import config
from Assignment import Assignment, Assignments
from dateutil import parser
import i18n

assignment_key = "assignments"
locale_key = 'locale'


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


def get_assignments(assignments: Assignments, descending=False) -> str:
    if assignments is None or len(assignments) == 0:
        return "目前没有作业 ;-)"
    message = "目前有{}项作业 \n".format(len(assignments))
    if descending:
        assignment_detail = ""
        for assignment in assignments:
            assignment_detail = str(assignment) + "\n" + assignment_detail
        message += assignment_detail
    else:
        for assignment in assignments:
            message += str(assignment)
            message += "\n"
    return message


# Display all assignments
def all_assignments(update: Update, context):
    if locale_key not in context.chat_data.keys():
        context.chat_data[locale_key] = update.effective_user.language_code
    assignments = context.chat_data.get(assignment_key)
    if len(context.args) == 1 and context.args[0] == "desc":
        reply_message = get_assignments(assignments, descending=True)
    else:
        reply_message = get_assignments(assignments, descending=False)
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


def daily_assignment_alert(context: CallbackContext):
    dp = context.dispatcher
    for chat_id, chat_data in dp.chat_data.items():
        reply_message = ""
        assignments = chat_data.get(assignment_key)
        if assignments is None:
            continue
        reply_message += get_assignments(assignments)
        context.bot.send_message(chat_id=chat_id, text=reply_message)


# Add Something
def add(update, context):
    assignment = Assignment(context.args[0], parser.parse(" ".join(context.args[1:])))
    if assignment_key not in context.chat_data.keys():
        context.chat_data[assignment_key] = Assignments()
    if locale_key not in context.chat_data.keys():
        context.chat_data[locale_key] = update.effective_user.language_code
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
    if locale_key not in context.chat_data.keys():
        context.chat_data[locale_key] = update.effective_user.language_code
    assignments = context.chat_data.get(assignment_key)
    reply_message = assignments[id].detail_str
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


def stop(update, context):
    """
    Stop the bot from sending alerts if there isn't any Assignment left.
    :param update:
    :param context:
    :return:
    """
    if assignment_key not in context.chat_data.keys():
        # This should be an error because there is no assignments object for this user.
        raise KeyError("This conversation don't have a assignments object")
    assignments = context.chat_data.get(assignment_key)
    if len(assignments) > 0:
        reply_text = "There is assignment left. Please empty all the assignments before stopping the bot."
        context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)
    else:
        context.chat_data.pop(assignment_key)
        reply_text = "Bot successfully stopped."
        context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)


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
            all_assignments,
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
    updater.dispatcher.add_handler(
        CommandHandler(
            'stop',
            stop,
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
