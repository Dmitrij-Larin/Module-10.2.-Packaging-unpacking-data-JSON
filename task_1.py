import json
import pickle


class Car:

    def __init__(self, brand, model, release, color):
        self.__brand = brand
        self.__model = model
        self.__release = release
        self.__color = color

    def get_brand(self):
        return self.__brand

    def get_model(self):
        return self.__model

    def get_release(self):
        return self.__release

    def get_color(self):
        return self.__color

    def type_car(self, type_car):
        return f"Тип автомобиля {self.__brand} {self.__model} - {type_car}"

    def change_color(self, new_color):
        self.__color = new_color
        return f"Автомобиль перекрашен в {new_color} цвет."


class CarEncoder(json.JSONEncoder):

    def default(self, o):
        return {
            "Бренд автомобиля": o.get_brand(),
            "Модель автомобиля": o.get_model(),
            "Год выпуска": o.get_release(),
            "Цвет": o.get_color(),
            "Доп-информация об автомобиле": o.type_car("внедорожник"),
            "Изменения": o.change_color("красный")
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
    car = Car('BMW', 'X5', 2024, 'синий')

    #JSON
    json_data = json.dumps(car, cls=CarEncoder, ensure_ascii=False, indent=2)
    print(json_data)
    python_car_from_string = json.loads(json_data)
    print(python_car_from_string)

    with open(r'json_files\car_info.json', 'w', encoding='utf-8') as fh:
        json.dump(car, fh, cls=CarEncoder, ensure_ascii=False, indent=2)

    with open(r'json_files\car_info.json', 'r', encoding='utf-8') as fh:
        python_car_from_file = json.load(fh)
    print(python_car_from_file)

    #pickle
    my_pickler_5 = MyPickler(protocol=5)
    my_pickler_default = MyPickler()

    car = my_pickler_5.pickle_data(car)
    car = MyUnpickler.unpickle_data(car)

    my_pickler_default.pickle_file('car_info', car)
    countries_and_capitals = MyUnpickler.unpickle_file('car_info.pkl')
