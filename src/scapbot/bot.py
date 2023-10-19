import datetime
import html
import json
import logging
import os
import random
import sys
import traceback

from pytz import timezone
from telegram import Message, Chat
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, ExtBot, ApplicationBuilder, ContextTypes, filters
from telegram.constants import ParseMode

from . import handlers

logging.StreamHandler(sys.stdout)
LEGGENDARY_DROP_RATE = 10
LEGGENDARY_IMAGE = "cazzate/magni.jpeg"
KEYBOARD = [["SI"], ["NO"]]
IMAGES_FOLDER = "cazzate/scap"


class ScapBot:
    def __init__(self, chat_id: str, test_chat_id: str, daily_coin: int, token) -> None:
        self.chat_id: str = chat_id
        self.test_chat_id: str = test_chat_id
        self.scap_dict: dict = {}
        self.scap_coin_reset: bool = False
        self.daily_coin: int = daily_coin
        self.token = token
        self.logger = logging.getLogger(self.chat_id)
        self.logger.setLevel(logging.DEBUG)

    # ERROR HANDLER
    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Log the error and send a telegram message to notify the developer."""
        # Log the error before we do anything else, so we can see it even if something breaks.
        self.logger.error("Exception while handling an update:", exc_info=context.error)

        # traceback.format_exception returns the usual python message about an exception, but as a
        # list of strings rather than a single string, so we have to join them together.
        tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
        tb_string = "".join(tb_list)

        # Build the message with some markup and additional information about what happened.
        # You might need to add some logic to deal with messages longer than the 4096-character limit.
        update_str = update.to_dict() if isinstance(update, Update) else str(update)
        message = (
            "An exception was raised while handling an update\n"
            f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
            "</pre>\n\n"
            f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
            f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
            f"<pre>{html.escape(tb_string)}</pre>"
        )

        # Finally, send the message
        await context.bot.send_message(
            chat_id=self.test_chat_id, text=message, parse_mode=ParseMode.HTML
        )

    def reset_scap_coin(self, context: ContextTypes.DEFAULT_TYPE):
        """Clears scap_dict and resets scap coins count"""
        self.scap_dict.clear()
        return context.bot.send_message(chat_id=self.chat_id, text="BUONGIORNO, SCAP COIN RESETTATI")

    # SCAP HANDLER
    async def scap(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Runs the scap command"""
        if not update.effective_user or not update.effective_chat:
            return ConversationHandler.END

        if not update.message:
            return ConversationHandler.END

        self.logger.info("Launching `scap` command")

        if not self.scap_coin_reset and context.job_queue:
            self.scap_coin_reset = True
            context.job_queue.run_daily(
                self.reset_scap_coin,
                datetime.time(hour=8, minute=0, tzinfo=timezone("Europe/Rome")),
                days=(0, 1, 2, 3, 4, 5, 6),
                chat_id=update.message.chat_id,
            )
            await context.bot.send_message(chat_id=update.effective_chat.id, text="reset SCAP COIN alle 8")

        user_name = update.effective_user.name
        if await self.update_coins(user_name, update.message):
            if await self.legendary_extraction(user_name, update.effective_chat, update.message, context.bot):
                return 0

            await self.send_photo(context.bot, update.effective_chat)
            await update.message.reply_text(f"SCAP COIN rimasti: {self.scap_dict[user_name]}")

        return ConversationHandler.END

    async def legendary_extraction(self, user_name: str, chat: Chat, message: Message, bot: ExtBot):
        """Extecutes the Leggendary image extraction

        Returns:
            bool: True if the leggendary image was extracted otherwise returns False
        """
        if random.randint(1, LEGGENDARY_DROP_RATE) != 1:
            return False

        await bot.send_message(chat_id=chat.id, text="wooo leggendaria!")
        with open(LEGGENDARY_IMAGE, "rb") as photo_file:
            await bot.send_photo(chat_id=chat.id, photo=photo_file)
        await message.reply_text(f"SCAP COIN rimasti: {self.scap_dict[user_name]}")
        await message.reply_text("Vuoi caricare un'immagine?", reply_markup=ReplyKeyboardMarkup(KEYBOARD, one_time_keyboard=True, selective=True))
        return True

    async def send_photo(self, bot: ExtBot, chat: Chat):
        """Extracts and sends an image"""
        img = random.choice(os.listdir(IMAGES_FOLDER))
        img_path = f"{IMAGES_FOLDER}/{img}"
        with open(img_path, "rb") as photo_file:
            return await bot.send_photo(chat_id=chat.id, photo=photo_file)

    async def update_coins(self, user_name: str, message: Message):
        """Updates scap coins count of the given user"""
        self.scap_dict[user_name] = self.scap_dict[user_name] - 1 if user_name in self.scap_dict else self.daily_coin - 1
        if self.scap_dict[user_name] == -1:
            await message.reply_text("SCAP COIN FINITI, se ne vuoi altri https://www.paypal.me/matteoartuso99")
            return False

        if self.scap_dict[user_name] == -10:
            await message.reply_text("CONGRATULAZIONI sei un COGLIONE")
            return False

        return self.scap_dict[user_name] >= -1

    def get_conversation_handler(self):
        """Returns the ConversationHandler for the scap command"""
        return ConversationHandler(
            entry_points=[CommandHandler("scap", self.scap)],
            states={
                0: [MessageHandler(filters.Regex(r'SI'), handlers.invia_immagine), MessageHandler(filters.Regex(r'NO'), handlers.rifiuta_invia_immagine)],
                1: [MessageHandler(filters.PHOTO, handlers.salva_immagine)],
            },
            fallbacks=[CommandHandler("cancel", handlers.cancel)],
            per_user=True,
            per_chat=False
        )

    def get_updater(self):
        """Returns the Updater used to run this instance of the Bot"""
        # Create the Updater and pass it your bot token.
        application = ApplicationBuilder().token(self.token).concurrent_updates(False).build()

        # Get the dispatcher to register handlers
        for command in handlers.COMMANDS:
            application.add_handler(CommandHandler(*command))

        application.add_handler(self.get_conversation_handler())
        application.add_error_handler(self.error_handler)

        return application
