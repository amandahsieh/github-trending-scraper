import pytest
from unittest.mock import patch

def test_telegram_key():
    with patch('src.bot.key.TELEGRAM_TOKEN', 'mock_token'):
        with patch('src.bot.key.CHAT_ID', 'mock_chat_id'):
            from src.bot.key import TELEGRAM_TOKEN, CHAT_ID
            
            # 檢查模擬的 token 和 chat_id 是否正確
            assert TELEGRAM_TOKEN == "mock_token", "Token should be 'mock_token'"
            assert CHAT_ID == "mock_chat_id", "Chat ID should be 'mock_chat_id'"
