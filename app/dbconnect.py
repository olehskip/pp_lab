from re import U
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from models import *
import pg8000


def loadSession():
    engine = create_engine("postgresql+pg8000://postgres:123456@localhost:5432/postgres", echo=False)
    
    metadata = MetaData(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    user1 = Users(surname="Skip", name="Oleg", username="sdfgsdfg", password="3f5j8903f5g6uj83f5guj890")
    user2 = Users(surname="Rusyn", name="Vasyl", username="sdfgsd", password="3f5uj93fgj3fj983fj89u3fj")
    session.add(user1)
    session.add(user2)
    session.commit()
    family_budget = FamilyBudgets(money_amount=100000)
    session.add(family_budget)
    session.commit()
    familybudgetconnection1 = FamilyBudgetsUsers(family_budget_id=family_budget.id, user_id=user1.id)
    familybudgetconnection2 = FamilyBudgetsUsers(family_budget_id=family_budget.id, user_id=user2.id)
    session.add(familybudgetconnection1)
    session.add(familybudgetconnection2)
    personal_budget1 = PersonalBudgets(id=user1.id, money_amount=10000)
    personal_budget2 = PersonalBudgets(id=user2.id, money_amount=20000)
    session.add(personal_budget1)
    session.add(personal_budget2)
    session.commit()
    operation1 = Operation(sender_id=user1.id, receiver_id=user2.id, sender_type="personal", receiver_type="personal", money_amount=1000, date="2021-05-01 12:00:00")
    operation2 = Operation(sender_id=user1.id, receiver_id=family_budget.id, sender_type="personal", receiver_type="family", money_amount=1000, date="2021-05-01 12:00:00")
    session.add(operation1)
    session.add(operation2)
    session.commit()
    return session

if __name__ == "__main__":
    session = loadSession()
    res = session.query(Users).all()
    print(res)
    res = session.query(FamilyBudgets).all()
    print(res)
    res = session.query(PersonalBudgets).all()
    print(res)
    res = session.query(FamilyBudgetsUsers).all()
    print(res)