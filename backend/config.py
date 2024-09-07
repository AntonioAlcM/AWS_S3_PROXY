import ujson


def load_secrets(filepath: str = "/run/secrets/backend_secrets"):
    """
    Loads secrets from a file.

    Args:
        filepath (str): The filepath of the secrets file.

    Returns:
        dict: The loaded secrets as a dictionary.

    """
    with open(filepath) as f:
        return ujson.load(f)
