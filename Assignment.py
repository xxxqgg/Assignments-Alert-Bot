class Assignment:
    _id_index = 0

    def __init__(self, title, due_time, *args, **kwargs):
        self.id = Assignment._id_index
        self.title = title
        self.due_time = due_time

        Assignment._id_index += 1

    def __str__(self):
        sdt = self.due_time
        str_time = str(sdt.month).zfill(2) + "-" + str(sdt.day).zfill(2) + " " + str(sdt.hour).zfill(2) + ":" + str(sdt.minute).zfill(2)
        return str(self.id) + "-" + self.title + " " + str_time