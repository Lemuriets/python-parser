from songs_parser import parse, write_to_txt


def main() -> None:
    try:
        url = input('Введите url сайта: ')

        parse(url)

        main()
    except KeyboardInterrupt:
        print('вы успешно вышли из программы')


if __name__  == '__main__':
    main()