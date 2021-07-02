import requests
from bs4 import BeautifulSoup

from decorators import check_http
from validation import Validation_url


class Parser:
    def __init__(self, url: str, write_to_console: bool = False, path: str = 'txt_files/') -> None:
        self.url = url
        self.path = path
        self.write_to_console = write_to_console
        self.song_name = self._gen_song_name_by_url(self.url)

        self._main()

    def _main(self) -> None:
        try:
            Validation_url(self.url)
        except AssertionError:
            return None

        if self._get_response(self.url) is None:
            return None

        html_content = self._get_html_content(self.song_name)

        text = self.parse(html_content)

        if text is None:
            return None

        self._write_text_to_file(self.path + self.song_name, text)

        if bool(self.write_to_console):
            print(text)

    @staticmethod
    def _write_text_to_file(path: str, text: str) -> None:
        try:
            with open(f'{path}.txt', 'w', encoding='utf-8') as txt_file:
                txt_file.write(text)
        except FileNotFoundError:
            print('не удалось записать текст в файл, проверьте правильность указанного пути')
            return None

    @staticmethod
    def _gen_song_name_by_url(url: str) -> str:
        song_name = url.split('/')[-1]

        if song_name.endswith('.html'):
            song_name = song_name.replace('.html', '')

        return song_name

    @staticmethod
    def _get_response(url: str):
        try:
            response = requests.get(url)
        except (
            requests.exceptions.MissingSchema,
            requests.exceptions.ConnectionError,
            requests.exceptions.InvalidSchema
        ):
            print('неверно указан url адрес или произошла ошибка при подключении')
            return None

        if response.status_code != 200:
            print('не удалось получить данные со страницы')
            return None

        return response

    @staticmethod
    def _write_html_content_to_file(content: str, filename: str) -> None:
        if filename == '':
            return None

        try:
            with open(f'html_files/{filename}.html', 'w', encoding='utf-8') as new_html_file:
                new_html_file.write(content)
        except FileNotFoundError:
            return None
    
    def _get_html_content(self, filename: str = None) -> str:
        if filename is None:
            html_content = self._get_response(self.url).text
            return html_content
        
        try:
            with open(f'html_files/{filename}.html', 'r', encoding='utf-8') as html_file:
                html_content = html_file.read()
        except FileNotFoundError:
            html_content = self._get_response(self.url).text
            self._write_html_content_to_file(html_content, self.song_name)

        if html_content.replace(' ', '') == '':
            html_content = self._get_response(self.url).text

        return html_content


    def parse(self, content: str) -> str:
        soup = BeautifulSoup(content, 'html.parser')

        original_text_list = []
        translate_text_list = []

        for tag in soup.find_all('div', class_='original'):
            if tag.get_text() == '':
                continue
            original_text_list.append(tag.get_text().replace('\n', ''))

        for tag in soup.find_all('div', class_='translate'):
            if tag.get_text() == '':
                continue
            translate_text_list.append(tag.get_text().replace('\n', ''))

        if (len(original_text_list) == 0) or (len(translate_text_list) == 0):
            print('не удалось получить перевод с указанной страницы, возможно, вы неверно указали url адрес')
            return None

        all_texts = list(zip(original_text_list, translate_text_list))

        ready_text = ''

        for orig, tran in all_texts:
            ready_text += orig + '\n'
            ready_text += tran + '\n' * 2

        return ready_text
