import yaml


def load_file(filepath: str):
    with open(filepath, "r") as f:
        file = f.read()
    return file


def read_yml(path):
    with open(path, 'r') as f:
        file = yaml.safe_load(f)
    return file