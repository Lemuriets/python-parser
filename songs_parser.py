from os import listdir, remove
import requests
from bs4 import BeautifulSoup

from decorators import check_http


def get_html_content(filename: str):
    if not filename.endswith('.html'):
        raise TypeError('Следует указывать файл с расширением .html')
    try:
        with open(f'html_files/{filename}', 'r', encoding='utf-8') as html_file:
            content = html_file.read()
    except FileNotFoundError:
        print('Неверно указан путь к файлу ')
        return None

    return content


@check_http
def gen_songname_by_url(url: str) -> str:
    filename = url.split('/')[-1]

    if filename.endswith('.html'):
        filename = filename.replace('.html', '')

    filename = filename.replace('.', '_')

    return filename


def write_to_txt(filename: str, text: list) -> None:
    with open(f'txt_files/{filename}.txt', 'w', encoding='utf-8') as txt_file:
        for i, j in text:
            txt_file.writelines(i + '\n')
            txt_file.writelines(j + '\n' * 2)
    
    print('Текст песни с переводом был успешно сохранен в файл')


def save_content_in_file(filename: str, content: str) -> None:
    try:
        with open(f'html_files/{filename}', 'w', encoding='utf-8') as file:
            file.write(content)
    except FileNotFoundError:
        print('Не удалось сохранить файл, возможно вы неверно указали путь к файлу')
        return None


def get_response(url: str, save_in_file: bool = True) -> requests.Response:
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.ConnectionError:
        raise requests.exceptions.ConnectionError('Указанный url адрес не существует или произошла ошибка при подключении')
    except requests.exceptions.MissingSchema:
        raise requests.exceptions.MissingSchema('Неверно указан url адрес')

    response.raise_for_status()

    if save_in_file:
        filename = gen_songname_by_url(url) + '.html'

        save_content_in_file(filename, response.text)

    return response


def parse(url: str) -> None:
    if not url.startswith('https://www.amalgama-lab.com/songs'):
        print('К сожалению, на данный момент парсер поддерживет только сайт amalgama-lab.com')
        return None

    filename = gen_songname_by_url(url) + '.html'

    if filename not in listdir('html_files'):
        get_response(url)

    content = get_html_content(filename)

    if content is None:
        return None

    soup = BeautifulSoup(content, 'html.parser')

    original_text_list = []
    translate_text_list = []

    for i in soup.find_all('div', class_='original'):
        if i.get_text() == '':
            continue
        original_text_list.append(i.get_text().replace('\n', ''))

    for i in soup.find_all('div', class_='translate'):
        if i.get_text() == '':
            continue
        translate_text_list.append(i.get_text().replace('\n', ''))


    all_text = list(zip(original_text_list, translate_text_list))

    if len(all_text) == 0:
        print('Программа не смогла получить текст песни, возможно вы неверно указали url адрес')

        remove(f'html_files/{filename}')

        return None

    write_to_txt(gen_songname_by_url(url), all_text)

    return None
