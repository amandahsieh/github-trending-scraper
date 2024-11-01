import pytest
from unittest.mock import patch
from src.utils.logger import log_error, log_info

@patch('src.utils.logger.logging.error')
def test_log_error(mock_logging_error):
    """
    測試 log_error 函數。
    """
    test_message = "This is an error message"
    
    # 執行 log_error 函數
    log_error(test_message)
    
    # 檢查 logging.error 是否被正確調用
    mock_logging_error.assert_called_once_with(test_message)

@patch('src.utils.logger.logging.info')
def test_log_info(mock_logging_info):
    """
    測試 log_info 函數。
    """
    test_message = "This is an info message"
    
    # 執行 log_info 函數
    log_info(test_message)
    
    # 檢查 logging.info 是否被正確調用
    mock_logging_info.assert_called_once_with(test_message)
