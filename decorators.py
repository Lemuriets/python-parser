def check_http(func):
    def wrapper(self, url: str):
        if (not url.startswith('http://')) and (not url.startswith('https://')):
            print('url адрес должен начинаться с http:// или https://')
            return False
        return func(self, url)
    return wrapper
