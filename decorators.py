def check_http(func):
    def wrapper(url: str):
        if (not url.startswith('http://')) and (not url.startswith('https://')):
            return None
        return func(url)
    return wrapper
