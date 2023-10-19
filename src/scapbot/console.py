import argparse
import os
import pathlib

from . import __VERSION__
from .bot import ScapBot

CHAT_ID = "-1001831422326"
TEST_CHAT_ID = "-845504008"
DEFAULT_DAILY_COINS = 1
DEFAULT_TOKEN_PATH = "token.txt"
DEFAULT_TEST_TOKEN_PATH = "test_token.txt"


def local_run(token_path: str, chat_id: str, test_chat_id: str,daily_coins: int):
    print("Launching ScapBot instance using these parameters:")
    print(f"Token Path: {token_path}")
    print(f"Chat ID: {chat_id}")
    print(f"Test Chat ID: {test_chat_id}")
    print(f"Daily Coins: {daily_coins}")
    token = pathlib.Path(token_path).read_text().strip()
    scap_bot = ScapBot(chat_id, test_chat_id, daily_coins, token)
    application = scap_bot.get_updater()

    # Start the Bot
    application.run_polling()


def console_run():
    """Function run when the package is called from the command line"""
    parser = argparse.ArgumentParser(prog="scapbot", description="Launches an instance of the ScapBot")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__VERSION__}")
    parser.add_argument(
        "--token",
        type=os.path.relpath,
        default=[None],
        nargs=1,
        required=False,
        dest="token_path",
        help=f"Relative path to the Token file (default: {DEFAULT_TOKEN_PATH})",
    )
    parser.add_argument(
        "--chatid",
        type=str,
        default=[None],
        nargs=1,
        required=False,
        dest="chat_id",
        help=f"Identifier of the telegram chat the bot should interact with (default: {CHAT_ID})",
    )
    parser.add_argument(
        "--testchatid",
        type=str,
        default=[None],
        nargs=1,
        required=False,
        dest="test_chat_id",
        help=f"Identifier of the telegram chat the bot should send errors report (default: {TEST_CHAT_ID})",
    )
    parser.add_argument(
        "--coins",
        type=int,
        default=[None],
        nargs=1,
        required=False,
        dest="coin",
        help=f"Specifies the amount of daily coins each user gets (default: {DEFAULT_DAILY_COINS})",
    )
    parser.add_argument(
        "--test", action="store_true", help="Specifies if a test instance should be run (Other default values might change in test runs)", default=False
    )

    args = parser.parse_args()
    token_path: str | None = args.token_path[0]
    is_test: bool = args.test
    chat_id: str | None = args.chat_id[0]
    test_chat_id: str | None = args.test_chat_id[0]
    coins: int | None = args.coin[0]

    # Parse Token Path
    if not token_path:
        token_path = DEFAULT_TEST_TOKEN_PATH if is_test else DEFAULT_TOKEN_PATH
    if not os.path.exists(token_path):
        print(f"Token could not be found at: {token_path}")
        return

    # Parse Chat ID
    if not chat_id:
        chat_id = TEST_CHAT_ID if is_test else CHAT_ID

    # Parse Test Chat ID
    if not test_chat_id:
        test_chat_id = TEST_CHAT_ID

    # Parse Daily Coins
    if not coins:
        coins = DEFAULT_DAILY_COINS

    local_run(token_path=token_path, chat_id=chat_id, test_chat_id=test_chat_id,daily_coins=coins)
