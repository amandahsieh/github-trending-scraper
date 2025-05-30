from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from src.services.fetch_service import fetch_and_save_repos
import os
import requests

class GithubTrendingBot:
    def __init__(self, token):
        self.app = Application.builder().token(token).build()
        self.token = token
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    async def handle_trending(self, update: Update, context: ContextTypes.DEFAULT_TYPE, period: str, language=None):
        """
        Handle trending command to fetch, send, and save GitHub trending data for the specified period and language.
        """
        await update.message.reply_text(f"Fetching {period} GitHub trending repositories for {language if language else 'all languages'}...")
        
        # Fetch and save the trending repositories
        data = await fetch_and_save_repos(period, language)

        if data:
            # Construct the message to send to Telegram
            message = f"{period.capitalize()} GitHub Trending for {language if language else 'all languages'}:\n" + '\n'.join(
                [f"{repo['author']} - {repo['url']} (🌟: {repo['stars']})" for repo in data[:10]]
            )
            await update.message.reply_text(message)
        else:
            await update.message.reply_text(f"No {period} trending repositories found for {language if language else 'all languages'}.")

    async def run(self):
        self.app.add_handler(CommandHandler('daily', lambda u, c: self.handle_trending(u, c, 'daily')))
        self.app.add_handler(CommandHandler('weekly', lambda u, c: self.handle_trending(u, c, 'weekly')))
        self.app.add_handler(CommandHandler('monthly', lambda u, c: self.handle_trending(u, c, 'monthly')))
        self.app.add_handler(CommandHandler('language', self.handle_language))
        await self.app.run_polling()

    async def handle_language(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle the /language command to fetch daily trending data for a specified language.
        """
        if context.args:
            language = context.args[0]
            await self.handle_trending(update, context, 'daily', language)
        else:
            await self.handle_trending(update, context, 'daily')  # Fetch for all languages if not specified

    async def send_trending_to_telegram(self, period: str, language=None):
        """
        Fetch, send, and save GitHub trending data for a specified period, without needing `update` or `context`.
        """
        # Fetch and save the trending repositories
        data = await fetch_and_save_repos(period, language)

        if data:
            # Construct the message to send to Telegram
            message = f"{period.capitalize()} GitHub Trending for {language if language else 'all languages'}:\n" + '\n'.join(
                [f"{repo['author']} - {repo['url']} (Stars: {repo['stars']})" for repo in data[:10]]
            )
            self.send_message(message)
        else:
            self.send_message(f"No {period} trending repositories found for {language if language else 'all languages'}.")

    def send_message(self, message):
        """
        Helper method to send a message to the configured Telegram chat.
        """
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message
        }
        requests.post(url, data=payload)
