import time

def benchmark(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()

        result = func(*args, **kwargs)

        end_time = time.perf_counter()
        print(f"Время выполениня функции {func.__name__}: {end_time - start_time}")
        return result
    return wrapper

def access_control(role):
    def check_role(func):
        def wrapper(*args, **kwargs):
            user = kwargs.get('current_user') if 'current_user' in kwargs else (args[1] if len(args) > 1 else None)

            if user != 'admin':
                raise PermissionError(f"Недостаточно прав пользователя {args[1]} для {func.__name__}")
            
            result = func(*args, **kwargs)
            return result
        return wrapper
    return check_role

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

        self.log(f"Добавление юзера ID={item.user_id} в БД")
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
    
    @access_control(role='admin')
    def delete_user(self, current_user, user_id):
        print("Пользователь УСПЕШНО УДАЛЕН!")

class BaseEngine:
    def log(self, message):
        print(f'[INFO]: Старт логгирования...')
        super().log(message)

class ConsoleLoggerMixin:
    def log(self, message):
        print(f'[INFO]: {message}')
        super().log(message)

class FileLoggerMixin:
    def log(self, message):
        print(f'[INFO]: Запись лога "{message}" в файл.')

class SmartDatabase(BaseEngine, Database, ConsoleLoggerMixin, FileLoggerMixin):
    pass

class FilterIterator:
    def __init__(self, database, **kwargs):
        self.database = database
        self.values = iter(database.users.values())
        self.filters = kwargs
        self.cursor = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        while True:
            try:
                user = next(self.values)
            except StopIteration:
                raise StopIteration
            if all(getattr(user, key, None) == value for key, value in self.filters.items()):
                return user
    
    @benchmark
    @staticmethod
    def stream_data(data_source, batch_size, **kwargs):
        batch = []
        for i in FilterIterator(data_source, **kwargs):
            batch.append(i)
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:
            yield batch

rec = Record(1,name='Svegrgay', age=16, pisipopi=23)
rec2 = Record(2, name='Oleg')
rec3 = Record(3, name='Sergay')

with SmartDatabase() as db:
    db(rec)
    db(rec2)
    db(rec3)