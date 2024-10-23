import json

def save_to_file(data: list, filename: str) -> None:
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4, sort_keys=True)
        print(f"Data saved to {filename}")
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")
