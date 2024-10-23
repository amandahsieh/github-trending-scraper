import pytest
import os
import json
from unittest.mock import patch
from tempfile import TemporaryDirectory
from src.utils.file_handler import save_to_file

# 測試 save_to_file 成功寫入資料
def test_save_to_file_success():
    data = [{"author": "test_author", "stars": 100}]

    # 使用 TemporaryDirectory 創建臨時目錄
    with TemporaryDirectory() as temp_dir:
        temp_file = os.path.join(temp_dir, "test_file.json")

        # 執行 save_to_file 函式
        save_to_file(data, temp_file)

        # 驗證文件是否存在
        assert os.path.exists(temp_file)

        # 驗證文件內容是否正確
        with open(temp_file, 'r') as f:
            content = json.load(f)
            assert content == data

# 測試 save_to_file 處理 IOError
@patch('builtins.open', side_effect=IOError("Failed to write file"))
def test_save_to_file_io_error(mock_open_func, capsys):
    data = [{"author": "test_author", "stars": 100}]

    with TemporaryDirectory() as temp_dir:
        temp_file = os.path.join(temp_dir, "test_file.json")

        # 執行 save_to_file 函式
        save_to_file(data, temp_file)

        # 驗證是否捕獲 IOError 並打印錯誤訊息
        captured = capsys.readouterr()
        assert f"Error writing to file {temp_file}: Failed to write file" in captured.out
