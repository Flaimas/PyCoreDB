class Record:
    def __init__(self, user_id, **kwargs):
        self.user_id = user_id
        self.fields = kwargs

    def __getattr__(self, item):
        if item in self.fields:
            return self.fields[item]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{item}'")

    def __eq__(self, other):
        if not isinstance(other, Record):
            return False
        return self.user_id == other.user_id

    def __str__(self):
        return str({'user_id': self.user_id, **self.fields})

    def __repr__(self):
        class_name = type(self).__name__
        kwargs_str = ", ".join(f"{k}={v!r}" for k, v in self.fields.items())
        separator = ", " if kwargs_str else ""
        return f"{class_name}({self.user_id}{separator}{kwargs_str})"

    def __call__(self, *args, **kwargs):
        return {'user_id': self.user_id, **self.fields}

class Database:
    def __init__(self):
        self.users = {}

    def __call__(self, item):
        if not isinstance(item, Record):
            raise ValueError(f"Ошибка! item не является объектом класса Record!")

        if item.user_id in self.users:
            raise ValueError(f"Ошибка! Объект с id={item.user_id} уже существует!")

        self.users[item.user_id] = item

    def __enter__(self):
        self._save_state = self.users.copy()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.users = self._save_state
            print(f"Произошла ошибка: {exc_val}. Изменения не сохранены.\n"
                  f"Текущее состояние БД: {self.users}")
            return False
        print(f"Выход из контекстного менеджера. Сохраненные изменения: {self.users}")
        return True

class FilterIterator:
    def __init__(self, database, **kwargs):
        self.database = database
        self.values = list(database.users.values())
        self.filters = kwargs
        self.cursor = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self.cursor < len(self.values):
            user = self.values[self.cursor]
            self.cursor += 1
            if all(getattr(user, key, None) == value for key, value in self.filters.items()):
                return user
        raise StopIteration

rec = Record(1,name='Svegrgay', age=16, pisipopi=23)
rec2 = Record(2, name='Oleg')
rec3 = Record(3, name='Sergay')
print(rec==rec2)
print(rec, rec2)
print(repr(rec), repr(rec2))

with Database() as db:
    db(rec)
    db(rec2)
    db(rec3)
    db(Record(4, name='Slava', job='Drug seller'))

for i in FilterIterator(db, name='Svegrgay', pisipopi=22):
    print(i)