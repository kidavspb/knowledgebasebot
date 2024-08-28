import json


class ListManager:
    def __init__(self, filename, key_as_int=True):
        self.filename = filename
        self.key_as_int = key_as_int
        self.data = self.read_data()

    def read_data(self):
        with open(self.filename, 'r') as file:
            data = json.load(file)
            if self.key_as_int:
                return {int(key): value for key, value in data.items()}
            else:
                return data

    def write_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=2, ensure_ascii=False)

    def get_data(self):
        return self.data

    def set_data(self, new_data):
        self.data = new_data
        self.write_data()

    def add_data(self, key, value):
        self.data[key] = value
        self.write_data()

    def del_data(self, key):
        if key in self.data:
            del self.data[key]
            self.write_data()