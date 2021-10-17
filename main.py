import elo
import os

# Extra Python #
from slackclient import SlackClient


# https://www.fullstackpython.com/blog/build-first-slack-bot-python.html

# Constants
CHANNEL_ID = "pong"

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None


def main():
    """Always on routine listening for slack messages"""
    while True:
        pass


if __name__ == "__main__":
    main()
