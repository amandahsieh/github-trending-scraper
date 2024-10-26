from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging
import os
from datetime import datetime

class TelegramBot:
    def __init__(self, token, chat_id):
        self.app = ApplicationBuilder().token(token).build()
        self.chat_id = chat_id
        self.add_handlers()

    def add_handlers(self):
        """
        Add command handlers
        """
        self.app.add_handler(CommandHandler("daily", self.handle_daily))
        self.app.add_handler(CommandHandler("weekly", self.handle_weekly))
        self.app.add_handler(CommandHandler("monthly", self.handle_monthly))

    async def handle_daily(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /daily command and fetch daily GitHub trending
        """
        print("Handling /daily command")
        await self.fetch_and_send_trending(update, 'daily')
        print("Finished handling /daily command")

    async def handle_weekly(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /weekly command and fetch weekly GitHub trending
        """
        print("Handling /weekly command")
        await self.fetch_and_send_trending(update, 'weekly')
        print("Finished handling /weekly command")

    async def handle_monthly(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /monthly command and fetch monthly GitHub trending
        """
        print("Handling /monthly command")
        await self.fetch_and_send_trending(update, 'monthly')
        print("Finished handling /monthly command")

    async def fetch_and_send_trending(self, update: Update, period: str):
        """
        fetch GitHub trending in specified period and send the message
        """
        from src.api.fetch import fetch_repos  # 延遲導入
        from src.utils.file_handler import save_to_file

        await update.message.reply_text(f"Fetching {period} GitHub trending repositories...")
        try:
            repos = await fetch_repos(period=period)
            if repos:
                message = f"{period.capitalize()} GitHub Trending:\n" + '\n'.join(
                    [f"{repo['author']} - {repo['url']} (Stars: {repo['stars']})" for repo in repos[:5]]
                )
                await update.message.reply_text(message)
                if isinstance(repos, list):
                    filename = os.path.join(f"repos/{period}", f"{datetime.now().strftime('%Y%m%d')}.json")
                    save_to_file(repos, filename)
                else:
                    print("Error: Data is not serializable.")
            else:
                await update.message.reply_text(f"No {period} trending repositories found.")
        except Exception as e:
            logging.error(f"Failed to fetch {period} trending: {e}")
            await update.message.reply_text(f"Failed to fetch {period} trending repositories.")

    async def run(self):
        """
        Start Telegram bot in an asynchronous event loop
        """
        print("Starting bot...")

        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()

