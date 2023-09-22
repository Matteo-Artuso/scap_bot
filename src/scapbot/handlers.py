from telegram import Update, ReplyKeyboardRemove
from telegram.constants import ParseMode
from telegram.ext import ConversationHandler, ContextTypes
import html, json, traceback, shutil


# BOT HANDLERS FUNCTIONS
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    if not context.error or not isinstance(update, Update) or not update.message:
        return

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = f"""An exception was raised while handling an update\n
        <pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}
        </pre>\n\n
        <pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n
        <pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n
        <pre>{html.escape(tb_string)}</pre>"""

    # Finally, send the message
    await context.bot.send_message(chat_id="-845504008", text=message, parse_mode=ParseMode.HTML)
    await update.message.reply_text("errore")
    return


def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user and update.message:
        return update.message.reply_text(f"Hi {update.effective_user.first_name}!")


async def barletz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="ma ti dai fuoco")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="\U0001F525")


async def balez(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="__balez__")


async def arco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="in-che-senso")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="\U0001F921")


async def lucio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat:
        with open("cazzate/lucio.mp3", "rb") as audio_file:
            await context.bot.send_audio(chat_id=update.effective_chat.id, audio=audio_file)


async def giorgio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="\U0001F441\U0001F444\U0001F441")


async def billy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Chiedere può essere la vergogna di un minuto, non chiedere il rimpianto di una vita. Mi fai assaggiare?"
        )


async def heroku(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="\U0001F4A9")


async def bergamo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat:
        with open("cazzate/bergamo.jpeg", "rb") as photo_file:
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_file)


async def tessera(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="F for tessera")


async def telecom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="@giu176 @riccardo17101907 @Befra22")


async def invia_immagine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        if update.message.text == "SI":
            await update.message.reply_text("Manda l'immagine", reply_markup=ReplyKeyboardRemove())
            return 1
        await update.message.reply_text("Menomale", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def salva_immagine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        file = await update.message.photo[-1].get_file()
        path = str(await file.download_to_drive())
        dest = f"cazzate/scap/{path}"
        shutil.move(path, dest)
        await update.message.reply_text("Immagine salvata")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message:
        await update.effective_message.reply_text("command canceled", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


COMMANDS = [
    ("start", start),
    ("barletz", barletz),
    ("balez", balez),
    ("arco", arco),
    ("lucio", lucio),
    ("giorgio", giorgio),
    ("billy", billy),
    ("heroku", heroku),
    ("bergamo", bergamo),
    ("tessera", tessera),
    ("telecom", telecom),
]


# def tessera(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     with open('utile/tessera.txt') as f:
#         text = f.read()
#     context.bot.send_message(chat_id=update.effective_chat.id, text=f"the one to rule them all ce l'ha {text}")


# def aule_libere_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.effective_user
#     if user.name == '@Artuzzo' or user.name == '@giu176' or user.name == '@andrebarl':
#         with open('utile/aule_libere.txt') as f:
#             text = f.read()
#         if text == "":
#             context.bot.send_message(chat_id=update.effective_chat.id, text='txt vuoto')
#         else:
#             context.bot.send_message(chat_id=update.effective_chat.id, text=text)
#         return 0
#     update.message.reply_text("utente non autorizzato")
#     return ConversationHandler.END


# def aule_libere_updated(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.effective_user
#     with open('utile/aule_libere.txt', 'w') as f:
#         f.write(update.message.text)
#     context.bot.send_message(chat_id=chat_id, text=f"{user.name} aule libere aggiornate")
#     return ConversationHandler.END


# def dov_e_ora(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [['billy'], ['giulio'], ['barletz']]
#     update.message.reply_text("chi vuoi sapere dov'è?", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, selective=True))
#     return 0


# def ora(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     giorno_ora = num_to_weekday(datetime.datetime.today().weekday())
#     now = datetime.datetime.now(timezone('Europe/Rome'))
#     if giorno_ora not in orari.orario[update.message.text].keys():
#         update.effective_message.reply_text("oggi non ha lezione", reply_markup=ReplyKeyboardRemove())
#         return ConversationHandler.END
#     if str(now.hour) not in orari.orario[update.message.text][str(giorno_ora)].keys():
#         update.effective_message.reply_text("ora non ha lezione", reply_markup=ReplyKeyboardRemove())
#         return ConversationHandler.END
#     update.effective_message.reply_text(orari.orario[update.message.text][str(giorno_ora)][str(now.hour)], reply_markup=ReplyKeyboardRemove())
#     return ConversationHandler.END


# def dove_sara(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [['billy'], ['giulio'], ['barletz']]
#     update.message.reply_text("chi vuoi sapere dov'è?", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, selective=True))
#     return 0


# def che_giorno(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     global chi
#     chi = update.message.text
#     keyboard = [['oggi'], ['LUN'], ['MAR'], ['MER'], ['GIO'], ['VEN']]
#     update.message.reply_text("che giorno vuoi sapere dov'è?", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, selective=True))
#     return 1


# def che_ora(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     global giorno
#     if update.message.text == 'oggi':
#         giorno = num_to_weekday(datetime.datetime.today().weekday())
#     else:
#         giorno = update.message.text
#     if giorno not in orari.orario[chi].keys():
#         update.effective_message.reply_text(giorno + " " + chi + " non ha lezione", reply_markup=ReplyKeyboardRemove())
#         return ConversationHandler.END
#     keyboard = [['8', '9'], ['10', '11'], ['12', '13'], ['14', '15'], ['16', '17'], ['18', '19']]
#     update.message.reply_text("a che ora vuoi sapere dov'è?", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, selective=True))
#     return 2


# def sara(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     global chi, giorno
#     now = update.message.text
#     if now not in orari.orario[chi][giorno].keys():
#         update.effective_message.reply_text(giorno + " alle " + now + " " + chi + " non ha lezione", reply_markup=ReplyKeyboardRemove())
#         return ConversationHandler.END
#     update.effective_message.reply_text(orari.orario[chi][giorno][now], reply_markup=ReplyKeyboardRemove())
#     chi = ''
#     giorno = ''
#     return ConversationHandler.END


# def tessera_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     update.effective_message.reply_text("chi ha ora LA tessera?")
#     return 0


# def tessera_updated(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.effective_user
#     with open('utile/tessera.txt') as f:
#         propietario_old = f.read()
#     with open('utile/tessera.txt', 'w') as f:
#         f.write(update.message.text)
#     context.bot.send_message(chat_id=chat_id, text=f"{user.name} the one to rule them all è passata da {propietario_old} a {update.message.text}")
#     return ConversationHandler.END


# def aule_libere(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     with open('utile/aule_libere.txt') as f:
#         text = f.read()
#     if text == "":
#         context.bot.send_message(chat_id=update.effective_chat.id, text='nessun aula salvata')
#     else:
#         context.bot.send_message(chat_id=update.effective_chat.id, text=text)
