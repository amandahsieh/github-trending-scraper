import os
import json
from unittest.mock import patch
from tempfile import TemporaryDirectory
from src.utils.file_handler import save_to_file

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
        assert os.path.exists(temp_file)
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
        save_to_file(data, temp_file)
        captured = capsys.readouterr()
        assert f"Error writing to file {temp_file}: Failed to write file" in captured.out
