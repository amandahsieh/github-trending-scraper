import json
import os

def save_to_file(data, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        raise IOError(f"Failed to save to {filepath}: {e}")

def read_from_file(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise IOError(f"Failed to read from {filepath}: {e}")
