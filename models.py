from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
from peewee import *

DATABASE = SqliteDatabase('journal.db')


class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

    def get_entries(self):
        return Entry.select().where(Entry.user == self)


    def get_tags(self, tag):
        return Entry.select().where(
            (Entry.user == self) & ((Entry.tag1==tag) | (Entry.tag2==tag)))

    @classmethod
    def create_user(cls, username, password):
        try:
            cls.create(
                username=username,
                password=generate_password_hash(password))
        except IntegrityError:
            raise ValueError("User already exists")


class Entry(Model):
    user = ForeignKeyField(
        model=User,
        backref='entries'
    )
    title = CharField()
    date = DateField()
    duration = IntegerField()
    learned = TextField()
    resources = TextField()
    tag1 = TextField()
    tag2 = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-date',)


def get_tags(tag):
    return Entry.select().where((Entry.tag1==tag) | (Entry.tag2==tag))



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Entry], safe=True)
    DATABASE.close()
