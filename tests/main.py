import pathlib
from scapbot import ScapBot
from telegram import Update

CHAT_ID = '-1831422326'
TEST_CHAT_ID = '-845504008'
MATTEO_TEST_CHAT_ID = '6184580723'
DAILY_COINS = 1
TOKEN = pathlib.Path("tests/token.txt").read_text()

# ## START ## #
if __name__ == '__main__':
    scap_bot = ScapBot(TEST_CHAT_ID, DAILY_COINS, TOKEN)
    application = scap_bot.get_updater()

    # Start the Bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)
