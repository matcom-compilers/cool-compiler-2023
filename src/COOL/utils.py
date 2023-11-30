
def load_file(filepath: str):
    with open(filepath, "r") as f:
        file = f.read()
    return file

def save_output(filepath: str, content: str):
    with open(filepath, "w") as f:
        f.write(content)