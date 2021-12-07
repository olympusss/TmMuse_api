from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from sqlalchemy.sql.expression import true
from models import (
    Users, CodeVerify, InterestItems, Interests, AddUserInterest, UserInterests,
    Banners, Categories, PhoneNumbers, PromotionStatuses, Images, Profiles,
    Ads, JoinCategoryAds
)
from tokens import create_access_token

def read_all_users(db: Session):
    result = db.query(
        Users.id,
        Users.fullname,
        Users.phone_number,
        Users.token,
        Users.created_at,
        Users.updated_at
    ).all()
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
    
def read_banner(db: Session):
    result = db.query(
        Banners.id,
        Banners.image,
        Banners.order,
        Banners.link,
        Banners.profile_id
    ).all()
    return result

def read_movies(db: Session):
    result = db.query(
        Profiles.nameTM,
        Profiles.nameRU,
        Profiles.short_descTM,
        Profiles.short_descRU,
        Images.small_image
    ).join(Images, and_(Images.profile_id == Profiles.id, Images.isVR == False)).\
        filter(Profiles.category_id == 2).\
            order_by(desc(Profiles.updated_at)).\
                limit(20).all()
    return result

def read_promotions(db: Session):
    result = db.query(
        PromotionStatuses.id,
        PromotionStatuses.promotion_status,
        Profiles.id,
        Profiles.nameTM,
        Profiles.nameRU,
        Profiles.short_descTM,
        Profiles.short_descRU,
        Profiles.instagram,
        Profiles.site,
        Profiles.like,
        Profiles.dislike,
        Images.small_image,
        Images.large_image,
        PhoneNumbers.phone_number
    ).join(Profiles, Profiles.id == PromotionStatuses.profile_id).\
        join(Images, and_(Images.profile_id == Profiles.id, Images.isVR == False)).\
            join(PhoneNumbers, PhoneNumbers.profile_id == Profiles.id).\
                order_by(desc(PromotionStatuses.updated_at)).all()
    return result
                
def read_ads(db: Session):
    result = db.query(
        Ads.id,
        Ads.name,
        Ads.comment_of_admin,
        Ads.image,
        Ads.profile_id,
        Ads.is_main
    ).filter(Ads.is_main == True).all()
    return result

def read_categories_by_ads(db: Session, ads_id):
    result = db.query(
        Categories.name
    ).join(JoinCategoryAds, and_(JoinCategoryAds.category_id == Categories.id, JoinCategoryAds.ads_id == ads_id)).\
        all()
    return result
    