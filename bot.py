from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters
import os

# Fetch Telegram Bot API Token from environment variable
TOKEN = os.getenv('TELEGRAM_BOT_API_TOKEN')

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Add GitHub Repo", callback_data='add_github')],
        [InlineKeyboardButton("Set Environment Variables", callback_data='set_env')],
        [InlineKeyboardButton("Deploy Bot", callback_data='deploy_bot')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Welcome! Choose an option:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if query.data == 'add_github':
        query.edit_message_text(text="Please provide the GitHub repository link:")
    elif query.data == 'set_env':
        query.edit_message_text(text="Please provide the environment variable key and value in the format 'KEY=VALUE':")
    elif query.data == 'deploy_bot':
        query.edit_message_text(text="Please provide the Dockerfile or other deployment instructions:")

def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if 'github.com' in text:
        # Handle GitHub repository link
        update.message.reply_text(f"GitHub repository added: {text}")
        # Add logic to store repository and process Dockerfile or other necessary actions
    elif '=' in text:
        # Handle environment variable setting
        key, value = text.split('=', 1)
        os.environ[key] = value
        update.message.reply_text(f"Environment variable set: {key}={value}")
    else:
        # Handle Dockerfile or other instructions
        update.message.reply_text(f"Deployment instructions received:\n{text}")
        # Add logic to handle deployment using Dockerfile or other methods

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
