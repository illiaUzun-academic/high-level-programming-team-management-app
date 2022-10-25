from mongoengine import StringField, Document, IntField


class Team(Document):
    name = StringField()
    office_location = StringField()


class Employee(Document):
    team_id = StringField()
    name = StringField()
    surname = StringField()
    salary = IntField()
    tenure = IntField()
