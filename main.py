from src.bot import ScapBot

CHAT_ID = '-1001831422326'
DAILY_COINS = 1

with open("token.txt") as token_file:
    TOKEN = token_file.readline()


# ## START ## #
if __name__ == '__main__':
    scap_bot = ScapBot(CHAT_ID, DAILY_COINS, TOKEN)
    updater = scap_bot.get_updater()

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
