from decorators import check_http


class Validation_url:
    def __init__(self, url: str):
        self.url = url

        assert self._validation(self.url)

    @check_http
    def _validation(self, url: str) -> bool:
        if not url.startswith('https://www.amalgama-lab.com'):
            print('парсер поддерживает только сайт www.amalgama-lab.com')
            return False
        return True
