from sqlalchemy import Column, String, Integer, Date

from .entity import Entity, Base
from marshmallow import Schema, fields

class Voter(Entity, Base):
    __tablename__ = 'voter'

    SSN = Column(String, primary_key=True)
    name = Column(String)
    birthday = Column(Date)
    gender = Column(String)
    ethnicity = Column(String)
    income = Column(Integer)
    party = Column(String, nullable=True)

    def __init__(self, SSN, name, birthday, gender, ethnicity, income, party):
        Entity.__init__(self)
        self.SSN = SSN
        self.name = name
        self.birthday = birthday
        self.gender = gender
        self.ethnicity = ethnicity
        self.income = income
        self.party = party

class VoterSchema(Schema):
    SSN = fields.Str()
    name = fields.Str()
    birthday = fields.DateTime()
    gender = fields.Str()
    ethnicity = fields.Str()
    income = fields.Number()
    party = fields.Str()
    created = fields.DateTime()




