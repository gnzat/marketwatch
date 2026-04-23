from telegram.ext import ApplicationBuilder, CommandHandler
from config import TELEGRAM_BOT_TOKEN, validate_config
from bot_handlers import start_command, brief_command

def main():
    validate_config()

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("brief", brief_command))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()