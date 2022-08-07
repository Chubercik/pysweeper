import json


def read_json(file_name: str) -> dict:
    """
    Reads a json file and returns a dictionary.
    """
    with open(file_name, 'r') as f:
        return json.load(f)


def write_json(file_name: str, data: dict, indent: int = 4) -> None:
    """
    Writes to a json file.
    """
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=indent)


def main() -> None:
    pass


if __name__ == "__main__":
    main()
