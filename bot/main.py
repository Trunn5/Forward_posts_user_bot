import asyncio

from bot.loader import app

import handlers


def main():
    print("Bot started.")
    app.run()


if __name__ == '__main__':
    asyncio.run(main())
