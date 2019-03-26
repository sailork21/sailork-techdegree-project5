import datetime

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
from peewee import *

DATABASE = SqliteDatabase('journal.db')

class Entry(Model):
    title = CharField(unique=True)
    date = CharField()
    duration = IntegerField()
    learned = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-date',)

    @classmethod
    def create_entry(cls, title, date, duration, learned, resources):
        with DATABASE.transaction():
                cls.create(
                    title = title,
                    date = date,
                    duration = duration,
                    learned = learned,
                    resources = resources)



def get_list():
    return Entry.select()

def edit_entry(id, title, date, duration, learned, resources):
    with DATABASE.transaction():
            cls.save(
                id = id,
                title = title,
                date = date,
                duration = duration,
                learned = learned,
                resources = resources)




def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()
