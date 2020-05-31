class Assignment:
    _id_index = 0

    def __init__(self, title, due_time, *args, **kwargs):
        self.id = Assignment._id_index
        self.title = title
        self.due_time = due_time

        Assignment._id_index += 1

    def __str__(self):
        return str(self.id) + "-" + self.title + " " + str(self.due_time)
