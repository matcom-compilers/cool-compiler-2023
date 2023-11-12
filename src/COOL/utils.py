

def load_file(filepath: str):
    with open(filepath, "r") as f:
        file = f.read()
    return file