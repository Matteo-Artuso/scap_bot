import logging
from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters
import Token
from os import listdir
import random

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


# BOT HANDLERS FUNCTIONS
def error_handler(update: Update, context: CallbackContext) -> None:
    """Log the error and send a telegram message"""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    context.bot.send_message(chat_id=update.effective_chat.id, text="riprova")


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_text(f"Hi {user.first_name}!")


def aule_libere(update: Update, context: CallbackContext):
    with open('orari/aule_libere.txt') as f:
        text = f.read()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def aule_libere_update(update: Update, context: CallbackContext):
    user = update.effective_user
    if user.first_name == 'Artuzzo' or user.first_name == 'giu176':
        with open('orari/aule_libere.txt') as f:
            text = f.read()
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        context.bot.send_message(chat_id=update.effective_chat.id, text="rispondi a questo msg con il nuovo orario")
        return 0
    update.message.reply_text("utente non autorizzato")
    return ConversationHandler.END


def aule_libere_updated(update: Update, context: CallbackContext):
    with open('orari/aule_libere.txt', 'w') as f:
        f.write(update.message.text)
    update.effective_message.reply_text("ok")
    return ConversationHandler.END


def barletz(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="ma ti dai fuoco")
    context.bot.send_message(chat_id=update.effective_chat.id, text=u"\U0001F525")


def arco(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=u"\U0001F921")


def lucio(update: Update, context: CallbackContext):
    context.bot.send_audio(chat_id=update.effective_chat.id, audio=open('cazzate/lucio.mp3', 'rb'))


def heroku(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=u"\U0001F4A9")


def giorgio(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=u"\U0001F441\U0001F444\U0001F441")


def scap(update: Update, context: CallbackContext):
    scap_img_list = listdir('cazzate/scap')
    lung = len(scap_img_list)
    lung = lung-1
    weights = []
    for img in scap_img_list:
        if img == 'magni.jpeg':
            weights.append(0.01)
        else:
            weights.append(0.99 / lung)
    scelta = random.choices(population=scap_img_list, weights=weights)
    if scelta == ['magni.jpeg']:
        context.bot.send_message(chat_id=update.effective_chat.id, text="wooo easter egg")
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('cazzate/scap/' + ''.join(scelta), 'rb'))


# unused function but necessary as fallback
def cancel(update: Update, context: CallbackContext):
    update.effective_message.reply_text("command canceled", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


### START ###
# Create the Updater and pass it your bot token.
updater = Updater(Token.token)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# handlers
aule_libere_update_handler = ConversationHandler(
    entry_points=[CommandHandler("aule_libere_update", aule_libere_update)],
    states={
        0: [MessageHandler(Filters.text & ~Filters.command, aule_libere_updated)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("aule_libere", aule_libere))
dispatcher.add_handler(CommandHandler("barletz", barletz))
dispatcher.add_handler(CommandHandler("arco", arco))
dispatcher.add_handler(CommandHandler("lucio", lucio))
dispatcher.add_handler(CommandHandler("heroku", heroku))
dispatcher.add_handler(CommandHandler("giorgio", giorgio))
dispatcher.add_handler(CommandHandler("scap", scap))
dispatcher.add_handler(aule_libere_update_handler)

dispatcher.add_error_handler(error_handler)

# Start the Bot
updater.start_polling()

# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()
