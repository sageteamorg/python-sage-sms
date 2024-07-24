import toml

def load_settings(toml_file):
    with open(toml_file, 'r') as f:
        config = toml.load(f)
    return config
