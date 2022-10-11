import logging
from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters
import Token
from os import listdir
import random
import utile.orario as orari
import datetime

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

#chat_id = ''


# UTILITY FUNCTIONS
def num_to_weekday(day):
    if day == 0:
        return 'LUN'
    if day == 1:
        return 'MAR'
    if day == 2:
        return 'MER'
    if day == 3:
        return 'GIO'
    if day == 4:
        return 'VEN'
    if day == 5:
        return 'SAB'
    if day == 6:
        return 'DOM'


def reset_scap_coin(context: CallbackContext):
    SCAP.clear()
#    context.bot.send_message(chat_id=chat_id, text="BUONGIORNO, SCAP COIN RESETTATI")


# BOT HANDLERS FUNCTIONS
def error_handler(update: Update, context: CallbackContext):
    """Log the error and send a telegram message"""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    update.message.reply_text("riprova")


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_text(f"Hi {user.first_name}!")


def aule_libere(update: Update, context: CallbackContext):
    with open('utile/aule_libere.txt') as f:
        text = f.read()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


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
    user = update.effective_user
    if user.name in SCAP.keys():
        SCAP[user.name] = SCAP[user.name] - 1
        if SCAP[user.name] == -1:
            update.message.reply_text("SCAP COIN FINITI, se ne vuoi altri https://www.paypal.me/matteoartuso99")
            return
        if SCAP[user.name] == -10:
            update.message.reply_text("CONGRATULAZIONI sei un coglione, hai usato /scap 10 volte in più del limite")
            return
        if SCAP[user.name] < -1:
            return
    else:
        SCAP[user.name] = 9
    scap_img_list = listdir('cazzate/scap')
    lung = len(scap_img_list)
    lung = lung-1   # magni escluso dal conteggio
    weights = []
    for img in scap_img_list:
        if img == 'magni.jpeg':
            weights.append(0.01)
        else:
            weights.append(0.99 / lung)
    scelta = random.choices(population=scap_img_list, weights=weights)
    if scelta == ['magni.jpeg']:
        context.bot.send_message(chat_id=update.effective_chat.id, text="wooo leggendaria!")
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('cazzate/scap/' + ''.join(scelta), 'rb'))
    update.message.reply_text("SCAP COIN rimasti: " + str(SCAP[user.name]))


def tessera(update: Update, context: CallbackContext):
    with open('utile/tessera.txt') as f:
        text = f.read()
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"the one to rule them all ce l'ha {text}")


def aule_libere_update(update: Update, context: CallbackContext):
    user = update.effective_user
    if user.name == '@Artuzzo' or user.name == '@giu176' or user.name == '@andrebarl':
        with open('utile/aule_libere.txt') as f:
            text = f.read()
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        context.bot.send_message(chat_id=update.effective_chat.id, text="rispondi a questo msg con il nuovo orario")
        return 0
    update.message.reply_text("utente non autorizzato")
    return ConversationHandler.END


def aule_libere_updated(update: Update, context: CallbackContext):
    with open('utile/aule_libere.txt', 'w') as f:
        f.write(update.message.text)
    update.effective_message.reply_text("ok")
    return ConversationHandler.END


def dov_e_ora(update: Update, context: CallbackContext):
    keyboard = [['artuzzo'], ['giulio'], ['barletz']]
    update.message.reply_text("chi vuoi sapere dov'è?", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, selective=True))
    return 0


def ora(update: Update, context: CallbackContext):
    giorno_ora = num_to_weekday(datetime.datetime.today().weekday())
    now = datetime.datetime.now()
    if giorno_ora not in orari.orario[update.message.text].keys():
        update.effective_message.reply_text("oggi non ha lezione", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    if str(now.hour) not in orari.orario[update.message.text][str(giorno_ora)].keys():
        update.effective_message.reply_text(f"alle {str(now.hour)} non ha lezione", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    update.effective_message.reply_text(orari.orario[update.message.text][str(giorno_ora)][str(now.hour)], reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def dove_sara(update: Update, context: CallbackContext):
    keyboard = [['artuzzo'], ['giulio'], ['barletz']]
    update.message.reply_text("chi vuoi sapere dov'è?", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, selective=True))
    return 0


def che_giorno(update: Update, context: CallbackContext):
    global chi
    chi = update.message.text
    keyboard = [['oggi'], ['LUN'], ['MAR'], ['MER'], ['GIO'], ['VEN']]
    update.message.reply_text("che giorno vuoi sapere dov'è?", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, selective=True))
    return 1


def che_ora(update: Update, context: CallbackContext):
    global giorno
    if update.message.text == 'oggi':
        giorno = num_to_weekday(datetime.datetime.today().weekday())
    else:
        giorno = update.message.text
    if giorno not in orari.orario[chi].keys():
        update.effective_message.reply_text(giorno + " " + chi + " non ha lezione", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    keyboard = [['8', '9'], ['10', '11'], ['12', '13'], ['14', '15'], ['16', '17'], ['18', '19']]
    update.message.reply_text("a che ora vuoi sapere dov'è?", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, selective=True))
    return 2


def sara(update: Update, context: CallbackContext):
    global chi, giorno
    now = update.message.text
    if now not in orari.orario[chi][giorno].keys():
        update.effective_message.reply_text(giorno + " alle " + now + " " + chi + " non ha lezione", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    update.effective_message.reply_text(orari.orario[chi][giorno][now], reply_markup=ReplyKeyboardRemove())
    chi = ''
    giorno = ''
    return ConversationHandler.END


def tessera_update(update: Update, context: CallbackContext):
    user = update.effective_user
    update.effective_message.reply_text("chi ha ora LA tessera?")
    return 0


def tessera_updated(update: Update, context: CallbackContext):
    with open('utile/tessera.txt', 'w') as f:
        f.write(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"the one to rule them all ce l'ha {update.message.text}")
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    update.effective_message.reply_text("command canceled", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


### START ###
chi = ''
giorno = ''
SCAP = {}
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

dov_e_ora_handler = ConversationHandler(
    entry_points=[CommandHandler("dov_e_ora", dov_e_ora)],
    states={
        0: [MessageHandler(Filters.text & ~Filters.command, ora)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

dove_sara_handler = ConversationHandler(
    entry_points=[CommandHandler("dove_sara", dove_sara)],
    states={
        0: [MessageHandler(Filters.text & ~Filters.command, che_giorno)],
        1: [MessageHandler(Filters.text & ~Filters.command, che_ora)],
        2: [MessageHandler(Filters.text & ~Filters.command, sara)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)


tessera_handler = ConversationHandler(
    entry_points=[CommandHandler("tessera_update", tessera_update)],
    states={
        0: [MessageHandler(Filters.text & ~Filters.command, tessera_updated)],
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
dispatcher.add_handler(CommandHandler("tessera", tessera))
dispatcher.add_handler(aule_libere_update_handler)
dispatcher.add_handler(dov_e_ora_handler)
dispatcher.add_handler(dove_sara_handler)
dispatcher.add_handler(tessera_handler)

dispatcher.add_error_handler(error_handler)

# Start the Bot
updater.start_polling()

# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()

j = updater.job_queue
job_daily = j.run_daily(reset_scap_coin, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(hour=8, minute=00, second=00))
