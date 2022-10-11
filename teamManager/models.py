from mongoengine import StringField, Document


# Create your models here.
class Team(Document):
    name = StringField()
    office_location = StringField()


class Worker(Document):
    name = StringField()
    surname = StringField()
