import json
import pickle


class Book:

    def __init__(self, title, author, release):
        self.__title = title
        self.__author = author
        self.__release = release

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_release(self):
        return self.__release

    def year_of_purchase(self, year):
        return f"Книга \"{self.__title}\" была куплена мной в {year} году."

    def pages_read(self, pages_read, pages):
        return f"Было прочитано {pages_read} страниц из {pages}"


class BookEncoder(json.JSONEncoder):

    def default(self, o):
        return {
            "Назваеие книги": o.get_title(),
            "Автор произведения": o.get_author(),
            "Год выхода": o.get_release(),
            "Когда я её приобрел": o.year_of_purchase(2017),
            "Прочитано страниц": o.pages_read(95, 256)
        }


class MyPickler:

    def __init__(self, protocol=pickle.DEFAULT_PROTOCOL):

        if protocol < 0 or protocol > 5:
            self.protocol = pickle.DEFAULT_PROTOCOL
        elif protocol == 0:
            self.protocol = pickle.HIGHEST_PROTOCOL
        else:
            self.protocol = protocol

    def pickle_data(self, data: object):
        pickled_data = pickle.dumps(data, self.protocol)
        return pickled_data

    def pickle_file(self, filename, data: object):
        with open(filename, 'wb') as fp:
            pickle.dump(data, fp, self.protocol)
        return f'Произведён пиклинг в файле {filename}'


class MyUnpickler:

    @classmethod
    def unpickle_data(cls, pickled_data):
        unpickle_data = pickle.loads(pickled_data)
        return unpickle_data

    @classmethod
    def unpickle_file(cls, pickled_filename):
        try:
            with open(pickled_filename, 'rb') as fp:
                unpickle_data = pickle.load(fp)
        except FileNotFoundError:
            return 'Файл не найден'
        return unpickle_data


if __name__ == '__main__':
    book = Book("Бойцовский клуб", "Чак Паланик", 1996)

    # JSON
    json_data = json.dumps(book, cls=BookEncoder, ensure_ascii=False, indent=2)
    print(json_data)
    python_car_from_string = json.loads(json_data)
    print(python_car_from_string)

    with open(r'json_files\book_info.json', 'w', encoding='utf-8') as fh:
        json.dump(book, fh, cls=BookEncoder, ensure_ascii=False, indent=2)

    with open(r'json_files\book_info.json', 'r', encoding='utf-8') as fh:
        python_car_from_file = json.load(fh)
    print(python_car_from_file)

    # pickle
    my_pickler_5 = MyPickler(protocol=5)
    my_pickler_default = MyPickler()

    book = my_pickler_5.pickle_data(book)
    book = MyUnpickler.unpickle_data(book)

    my_pickler_default.pickle_file('book_info', book)
    countries_and_capitals = MyUnpickler.unpickle_file('book_info.pkl')