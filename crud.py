from sqlalchemy.orm import Session
from models import (
    Users, CodeVerify, InterestItems, Interests, AddUserInterest, UserInterests
)
from tokens import create_access_token

def read_all_users(db: Session):
    result = db.query(Users).all()
    return result

def read_user_by_phone_number(db: Session, phone_number: str):
    result = db.query(
        Users.id,
        Users.fullname,
        Users.phone_number,
        Users.token
    ).filter(Users.phone_number == phone_number).first()
    return result

def create_user(db: Session, req: CodeVerify):
    newDict = {
        "fullname"      : req.fullname,
        "phone_number"  : req.phone_number
    }
    access_token = create_access_token(newDict)
    new_add = Users(
        fullname     = req.fullname,
        phone_number = req.phone_number,
        token        = access_token
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    if new_add:
        return True
    else:
        return False
    
    
def read_interests(db: Session):
    result = db.query(
        Interests.id,
        Interests.titleTM,
        Interests.titleRU
    ).all()
    return result

def read_interest_items_by_interest_id(db: Session, interest_id):
    result = db.query(
        InterestItems.id,
        InterestItems.titleTM,
        InterestItems.titleRU
    ).filter(InterestItems.interest_id == interest_id).all()
    
def create_user_interest_item(db: Session, user_id, item_id):
    new_add = UserInterests(user_id = user_id, interest_item_id = item_id)
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    if new_add:
        return True
    else:
        return False
    
def delete_user_interest(db: Session, user_id):
    delete = db.query(UserInterests).filter(UserInterests.user_id == user_id).\
        delete(synchronize_session=False)
    db.commit()
    if delete:
        return True
    else:
        return False