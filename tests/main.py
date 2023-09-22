from scapbot import ScapBot


CHAT_ID = '-1001831422326'
TEST_CHAT_ID = '6184580723'
DAILY_COINS = 1

with open("tests/tests_token.txt") as token_file:
    TOKEN = token_file.readline()


# ## START ## #
if __name__ == '__main__':
    scap_bot = ScapBot(TEST_CHAT_ID, DAILY_COINS, TOKEN)
    application = scap_bot.get_updater()

    # Start the Bot
    application.run_polling()
