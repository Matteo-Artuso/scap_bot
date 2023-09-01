from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, Filters, Updater
from telegram.bot import Bot
from telegram.message import Message
from telegram.chat import Chat
from pytz import timezone
import random, datetime, os, logging

from . import handlers


LEGGENDARY_DROP_RATE = 10
LEGGENDARY_IMAGE = "cazzate/magni.jpeg"
KEYBOARD = [["SI"], ["NO"]]
IMAGES_FOLDER = "cazzate/scap"


class ScapBot:
    def __init__(self, chat_id: str, daily_coin: int, token) -> None:
        self.chat_id: str = chat_id
        self.scap_dict: dict = {}
        self.scap_coin_reset: bool = False
        self.daily_coin: int = daily_coin
        self.token = token
        self.logger = logging.getLogger(self.chat_id)

    def reset_scap_coin(self, context: CallbackContext):
        """Clears scap_dict and resets scap coins count"""
        self.scap_dict.clear()
        context.bot.send_message(chat_id=self.chat_id, text="BUONGIORNO, SCAP COIN RESETTATI")

    def scap(self, update: Update, context: CallbackContext):
        """Runs the scap command"""
        if not update.effective_user or not update.effective_chat:
            return ConversationHandler.END

        if not self.scap_coin_reset and context.job_queue:
            self.scap_coin_reset = True
            context.job_queue.run_daily(
                self.reset_scap_coin,
                datetime.time(hour=8, minute=00, tzinfo=timezone("Europe/Rome")),
                days=(0, 1, 2, 3, 4, 5, 6),
                context=update.message.chat_id,
            )
            context.bot.send_message(chat_id=update.effective_chat.id, text="reset SCAP COIN alle 8")

        user_name = update.effective_user.name
        self.update_coins(user_name, update.message)

        if self.leggendary_extraction(user_name, update.effective_chat, update.message, context.bot):
            return 0

        self.send_photo(context.bot, update.effective_chat)
        #    update.message.reply_text("SCAP COIN rimasti: " + str(SCAP[user.name]))
        return ConversationHandler.END

    def leggendary_extraction(self, user_name: str, chat: Chat, message: Message, bot: Bot):
        """Extecutes the Leggendary image extraction

        Returns:
            bool: True if the leggendary image was extracted otherwise returns False
        """
        if random.randint(1, LEGGENDARY_DROP_RATE) != 1:
            return False

        bot.send_message(chat_id=chat.id, text="wooo leggendaria!")
        with open(LEGGENDARY_IMAGE, "rb") as photo_file:
            bot.send_photo(chat_id=chat.id, photo=photo_file)
        message.reply_text(f"SCAP COIN rimasti: {self.scap_dict[user_name]}")
        message.reply_text("Vuoi caricare un'immagine?", reply_markup=ReplyKeyboardMarkup(KEYBOARD, one_time_keyboard=True, selective=True))
        return True

    def send_photo(self, bot: Bot, chat: Chat):
        """Extracts and sends an image"""
        img = random.choices(population=os.listdir(IMAGES_FOLDER))
        with open(f"{IMAGES_FOLDER}/{''.join(img)}", "rb") as photo_file:
            bot.send_photo(chat_id=chat.id, photo=photo_file)

    def update_coins(self, user_name: str, message: Message):
        """Updates scap coins count of the given user"""
        self.scap_dict[user_name] = self.scap_dict[user_name] - 1 if user_name in self.scap_dict else self.daily_coin - 1
        if self.scap_dict[user_name] == -1:
            message.reply_text("SCAP COIN FINITI, se ne vuoi altri https://www.paypal.me/matteoartuso99")
            return
        if self.scap_dict[user_name] == -10:
            message.reply_text("CONGRATULAZIONI sei un COGLIONE")
            return
        if self.scap_dict[user_name] < -1:
            return

    def get_conversation_handler(self):
        """Returns the ConversationHandler for the scap command"""
        return ConversationHandler(
            entry_points=[CommandHandler("scap", self.scap, pass_job_queue=True)],
            states={
                0: [MessageHandler(Filters.text(["SI", "NO"]) & ~Filters.command, handlers.invia_immagine)],  # type: ignore
                1: [MessageHandler(Filters.photo & ~Filters.command, handlers.salva_immagine)],
            },
            fallbacks=[CommandHandler("cancel", handlers.cancel)],
        )

    def get_updater(self):
        """Returns the Updater used to run this instance of the Bot"""
        # Create the Updater and pass it your bot token.
        updater = Updater(self.token)

        # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher
        for command in handlers.COMMANDS:
            dispatcher.add_handler(CommandHandler(*command))

        dispatcher.add_handler(self.get_conversation_handler())
        dispatcher.add_error_handler(handlers.error_handler)

        return updater


# handlers
# aule_libere_update_handler = ConversationHandler(
#     entry_points=[CommandHandler("aule_libere_update", aule_libere_update)],
#     states={
#         0: [MessageHandler(Filters.text & ~Filters.command, aule_libere_updated)],
#     },
#     fallbacks=[CommandHandler('cancel', cancel)]
# )
# dov_e_ora_handler = ConversationHandler(
#     entry_points=[CommandHandler("dov_e_ora", dov_e_ora)],
#     states={
#         0: [MessageHandler(Filters.text & ~Filters.command, ora)],
#     },
#     fallbacks=[CommandHandler('cancel', cancel)]
# )
# dove_sara_handler = ConversationHandler(
#     entry_points=[CommandHandler("dove_sara", dove_sara)],
#     states={
#         0: [MessageHandler(Filters.text & ~Filters.command, che_giorno)],
#         1: [MessageHandler(Filters.text & ~Filters.command, che_ora)],
#         2: [MessageHandler(Filters.text & ~Filters.command, sara)],
#     },
#     fallbacks=[CommandHandler('cancel', cancel)]
# )
# tessera_handler = ConversationHandler(
#     entry_points=[CommandHandler("tessera_update", tessera_update)],
#     states={
#         0: [MessageHandler(Filters.text & ~Filters.command, tessera_updated)],
#     },
#     fallbacks=[CommandHandler('cancel', cancel)]
# )
