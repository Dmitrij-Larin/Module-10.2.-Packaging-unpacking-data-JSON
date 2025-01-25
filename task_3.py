import json
import pickle


class Stadium:

    def __init__(self, name, location, capacity):
        self.__name = name
        self.__location = location
        self.__capacity = capacity

    def get_name(self):
        return self.__name

    def get_location(self):
        return self.__location

    def get_capacity(self):
        return self.__capacity

    def __str__(self):
        return (f"Стадион {self.__name}, {repr(self.__location)}, {repr(self.__capacity)}")


class Location:

    def __init__(self, country):
        self.country = country

    def __repr__(self):
        return f"Растоложение: {self.country}"


class Capacity:

    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return f"Вместимость: {self.number} человек"


class JSONDataAdapter:

    @staticmethod
    def to_json(obj):
        if isinstance(obj, Stadium):
            return json.dumps({
                'Название': obj.get_name(),
                'Местоположение': obj.get_location().country,
                'Вместимость': obj.get_capacity().number,
            }, ensure_ascii=False, indent=2)

    @staticmethod
    def from_json(obj):
        obj = json.loads(obj)

        try:
            location = Location(obj['Местоположение'])
            capacity = Capacity(obj['Вместимость'])
            stadium = Stadium(obj['Название'], location, capacity)
            return stadium
        except AttributeError:
            print("Неверная структура!")


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
    location = Location("Лондон")
    capacity = Capacity(60704)
    stadium = Stadium("Эмирейтс", location=location, capacity=capacity)

    print(stadium)
    print()

    #JSON
    json_stadium = JSONDataAdapter.to_json(stadium)
    print(json_stadium)
    print()

    stadium_obj = JSONDataAdapter.from_json(json_stadium)
    print(stadium_obj)

    #pickle
    my_pickler_5 = MyPickler(protocol=5)
    my_pickler_default = MyPickler()

    stadium = my_pickler_5.pickle_data(stadium)
    stadium = MyUnpickler.unpickle_data(stadium)

    my_pickler_default.pickle_file('stadium_info', stadium)
    countries_and_capitals = MyUnpickler.unpickle_file('stadium_info.pkl')
