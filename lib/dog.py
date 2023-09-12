import sqlite3

CONN = sqlite3.connect(':memory:')
CURSOR = CONN.cursor()

class Dog:

    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed

    def create_table():
        sql = """CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
                )"""
        CURSOR.execute(sql)
        CONN.commit()

    def drop_table():
        sql = """DROP TABLE IF EXISTS dogs"""
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        if self.id:
            sql = "UPDATE dogs SET name=?, breed=? WHERE id=?"
            CURSOR.execute(sql, (self.name, self.breed, self.id))
        else:
            sql = "INSERT INTO dogs (name, breed) VALUES (?, ?)"
            CURSOR.execute(sql, (self.name, self.breed))
            self.id = CURSOR.lastrowid
        CONN.commit()
        return self

    def create(name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog

    def new_from_db(row):
        return Dog(row[1], row[2], row[0])

    def get_all():
        sql = "SELECT * FROM dogs"
        rows = CURSOR.execute(sql).fetchall()
        return [Dog.new_from_db(row) for row in rows]

    def find_by_name(name):
        sql = "SELECT * FROM dogs WHERE name = ?"
        row = CURSOR.execute(sql, (name,)).fetchone()
        return Dog.new_from_db(row) if row else None

    def find_by_id(id):
        sql = "SELECT * FROM dogs WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return Dog.new_from_db(row) if row else None

    def find_or_create_by(name, breed):
        dog = Dog.find_by_name(name)
        if dog:
            return dog
        else:
            return Dog.create(name, breed)

    def update(self):
        sql = "UPDATE dogs SET name = ?, breed = ? WHERE id = ?"
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()
