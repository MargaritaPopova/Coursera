import csv
from os import path


class CarBase:
    car_type = None

    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        return path.splitext(self.photo_file_name)[1]


class Car(CarBase):
    car_type = 'car'

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    car_type = 'truck'

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.body_whl = body_whl
        self.body_width = 0.0
        self.body_height = 0.0
        self.body_length = 0.0
        self.from_whl()

    def from_whl(self):
        if self.body_whl:
            whl = self.body_whl.split('x')
            if len(whl) != 3:
                return
            try:
                self.body_length = float(whl[0])
                self.body_width = float(whl[1])
                self.body_height = float(whl[2])
            except ValueError or TypeError:
                return

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):
    car_type = 'spec_machine'

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra


class Validator:

    def __init__(self, data: csv.DictReader):
        self.data = data

    def valid(self) -> bool:
        return all(x in ['car_type', 'brand', 'passenger_seats_count',
                         'photo_file_name', 'body_whl', 'carrying', 'extra'] for x in self.data.fieldnames)

    @staticmethod
    def validate_filename(name: str) -> bool:
        return path.splitext(name)[1] in ['.jpg', '.png', '.jpeg', '.tiff', '.gif', '.bmp', '.psd']

    def validate_base(self, row: dict) -> bool:
        return row['brand'] and row['photo_file_name'] and row['carrying'] \
               and self.validate_filename(row['photo_file_name'])

    def validate_car(self, row: dict) -> bool:
        return self.validate_base(row) and row['passenger_seats_count']

    def validate_spec(self, row: dict) -> bool:
        return self.validate_base(row) and row['extra']


def make_car_class(validator: Validator, row: dict) -> CarBase:
    if row['car_type'] == 'car' and validator.validate_car(row):
        return Car(row['brand'], row['photo_file_name'],
                   row['carrying'], row['passenger_seats_count'])
    elif row['car_type'] == 'truck' and validator.validate_base(row):
        return Truck(row['brand'], row['photo_file_name'],
                     row['carrying'], row['body_whl'])
    elif row['car_type'] == 'spec_machine' and validator.validate_spec(row):
        return SpecMachine(row['brand'], row['photo_file_name'],
                           row['carrying'], row['extra'])


def get_car_list(csv_filename):
    cars_list = []
    try:
        with open(csv_filename) as f:
            data = csv.DictReader(f, delimiter=';')
            validator = Validator(data)
            if not validator.valid():
                return []
            for row in data:
                vehicle = make_car_class(validator, row)
                if vehicle:
                    cars_list.append(vehicle)
    except FileNotFoundError:
        print('file not found')
    return cars_list


# if __name__ == '__main__':
#     for car in (get_car_list('coursera_week3_cars.csv')):
#         print(car.__dict__)
#     print(get_car_list('coursera_week3_cars.csv'))
    # truck = Truck('Nissan', 't1.jpg', '2.5', '2.4x2.3x2')
    # print(truck.body_width)
