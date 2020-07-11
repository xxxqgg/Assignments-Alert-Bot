class Assignment:
    _id_index = 0

    def __init__(self, title, due_time, *args, **kwargs):
        self.id = Assignment._id_index
        self.title = title
        self.due_time = due_time

        Assignment._id_index += 1

    def __str__(self):
        sdt = self.due_time
        str_time = str(sdt.month).zfill(2) + "-" + str(sdt.day).zfill(2) + " " + str(sdt.hour).zfill(2) + ":" + str(
            sdt.minute).zfill(2)
        return str(self.id) + "-" + self.title + " " + str_time

    @property
    def detail_str(self):
        return str(self.id) + " " + str(self.title) + "\n" + str(self.due_time)


class Assignments:
    """
    A class used for storing  Assignment objects
    """
    def __init__(self):
        self.data = dict()
        self.first_viable_index = 0

    def add(self, obj: Assignment):
        id = self.__get_first_viable_id()
        obj.id = id
        # Now we are hard coding the id for compatibility in the main.py file.
        # TODO: Hard coding id here maybe a bad idea. We should think about change this data structure later.
        self.data[id] = obj

    def __get_first_viable_id(self):
        while self.first_viable_index in self.data.keys():
            self.first_viable_index += 1
        return self.first_viable_index

    def remove(self, id: int):
        if id not in self.data.keys():
            raise KeyError("id({} is not in the current data)".format(id))
        obj = self.data.pop(id)
        if self.first_viable_index > id:
            self.first_viable_index = id
        return obj

    def __getitem__(self, item):
        return self.data[item]

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        data = sorted(self.data.values(), key=lambda x: x.due_time)
        return iter(data)
