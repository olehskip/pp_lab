from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, String, Column, ForeignKey, BigInteger, Identity
from sqlalchemy import Enum, DateTime, Boolean, Float, Date, Time

Base = declarative_base()

class FamilyBudgets(Base):
    __tablename__ = 'family_budgets'
    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True, nullable=False)
    money_amount = Column(BigInteger, nullable=False, default=0)

    def __repr__(self):
        return "<FamilyBudget(id='%s', money_amount='%s')>" % (
            self.id, self.money_amount)

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True, nullable=False)
    surname = Column(String(40), nullable=False)
    name = Column(String(40), nullable=False)
    username = Column(String(40), nullable=False, unique=True)
    password = Column(String(256), nullable=False)

    def __repr__(self):
        return "<User(id='%s', surname='%s', name='%s', username='%s', password='%s')>" % (
            self.id, self.surname, self.name, self.username, self.password)

class PersonalBudgets(Base):
    __tablename__ = 'personal_budgets'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
    money_amount = Column(BigInteger, nullable=False, default=0)

    def __repr__(self):
        return "<PersonalBudget(id='%s', money_amount='%s')>" % (
            self.id, self.money_amount)

class FamilyBudgetsUsers(Base):
    __tablename__ = 'family_budgets_users'
    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True, nullable=False)
    family_budget_id = Column(Integer, ForeignKey('family_budgets.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return "<FamilyBudgetsUsers(id='%s', user_id='%s', family_budget_id='%s')>" % (
            self.id, self.user_id, self.family_budget_id)

class Operation(Base):
    __tablename__ = 'operations'
    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True, nullable=False)
    sender_id = Column(Integer, nullable=False)
    receiver_id = Column(Integer, nullable=False)
    sender_type = Column(String(40), nullable=False)
    receiver_type = Column(String(40), nullable=False)
    money_amount = Column(BigInteger, nullable=False)
    date = Column(DateTime, nullable=False)