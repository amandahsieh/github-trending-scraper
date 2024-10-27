import os
import json
import pytest
from unittest.mock import patch
from tempfile import TemporaryDirectory
from src.utils.file_handler import save_to_file, read_from_file

def test_save_to_file_success():
    """
    Test case for successfully saving data using the save_to_file function.

    This test uses a temporary directory to simulate file creation.
    It verifies that the file is created and the content is correctly written.
    """
    data = [{"author": "test_author", "stars": 100}]
    with TemporaryDirectory() as temp_dir:
        temp_file = os.path.join(temp_dir, "test_file.json")
        save_to_file(data, temp_file)

        # 檢查文件是否存在
        assert os.path.exists(temp_file)

        # 檢查文件內容是否正確
        with open(temp_file, 'r') as f:
            content = json.load(f)
            assert content == data

@patch('builtins.open', side_effect=IOError("Failed to write file"))
def test_save_to_file_io_error(mock_open_func, capsys):
    """
    Test case for handling IOError in the save_to_file function.

    This test uses mocking to simulate an IOError during file writing.
    It verifies that the error is caught and the appropriate error message is printed.
    """
    data = [{"author": "test_author", "stars": 100}]
    with TemporaryDirectory() as temp_dir:
        temp_file = os.path.join(temp_dir, "test_file.json")

        # 嘗試保存文件並捕獲輸出錯誤
        with pytest.raises(IOError, match="Failed to write file"):
            save_to_file(data, temp_file)

def test_read_from_file_success():
    """
    Test case for successfully reading data from a file using the read_from_file function.

    This test uses a temporary directory to create a file and verify that it is read correctly.
    """
    data = [{"author": "test_author", "stars": 100}]
    with TemporaryDirectory() as temp_dir:
        temp_file = os.path.join(temp_dir, "test_file.json")

        # 寫入文件以測試讀取
        with open(temp_file, 'w') as f:
            json.dump(data, f)

        # 讀取文件並檢查內容
        read_data = read_from_file(temp_file)
        assert read_data == data

def test_read_from_file_not_exist():
    """
    Test case for handling file not found error in the read_from_file function.
    """
    with TemporaryDirectory() as temp_dir:
        temp_file = os.path.join(temp_dir, "non_existent_file.json")

        # 嘗試讀取不存在的文件並捕獲錯誤
        with pytest.raises(IOError, match="Failed to read from"):
            read_from_file(temp_file)

@patch('builtins.open', side_effect=IOError("Failed to read file"))
def test_read_from_file_io_error(mock_open_func):
    """
    Test case for handling IOError in the read_from_file function.

    This test uses mocking to simulate an IOError during file reading.
    It verifies that the error is raised.
    """
    with TemporaryDirectory() as temp_dir:
        temp_file = os.path.join(temp_dir, "test_file.json")

        # 嘗試讀取文件並捕獲輸出錯誤
        with pytest.raises(IOError, match="Failed to read file"):
            read_from_file(temp_file)
