#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Selutario <selutario@gmail.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv3

from pathlib import Path

from telegram.ext import Updater, CommandHandler, InlineQueryHandler, ChosenInlineResultHandler

from handlers import common_handlers, search_handlers
from handlers.delete_handlers import delete_conv_handler
from handlers.edit_handlers import edit_conv_handler
from handlers.upload_handlers import upload_conv_handler
from utils.common import settings


def main():
    # Start bot
    try:
        updater = Updater(token=Path(settings['token_path']).read_text().rstrip(), use_context=True)
    except Exception as e:
        print("Could not access token. Did you run the 'installer.py' first?")
        exit(1)

    dp = updater.dispatcher

    # Common commands - answer in Telegram
    dp.add_handler(CommandHandler("start", common_handlers.start))
    dp.add_handler(CommandHandler("random", common_handlers.get_random_video))

    # Conversation handlers
    dp.add_handler(upload_conv_handler)
    dp.add_handler(edit_conv_handler)
    dp.add_handler(delete_conv_handler)

    # Search & send video
    dp.add_handler(InlineQueryHandler(search_handlers.inline_search))
    dp.add_handler(ChosenInlineResultHandler(search_handlers.on_chosen_video))

    # log all errors
    dp.add_error_handler(common_handlers.error)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
