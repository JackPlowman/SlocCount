from os import getenv

PROJECT_URL = getenv("PROJECT_URL")
if PROJECT_URL is None:
    msg = "PROJECT_URL environment variable is not set"
    raise ValueError(msg)
