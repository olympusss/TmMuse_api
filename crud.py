from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from models import (
    Users, CodeVerify, InterestItems, Interests, UserInterests, Banners, 
    Categories, PhoneNumbers, PromotionStatuses, Images, Profiles, Ads, 
    JoinCategoryAds, GetProfile, Tags, TagProducts, Galleries, Posts,
    Certificates, PromoCodes, Inbox, SendUser, Answers, AnsweredMessages,
    CardUsers, Jobs, CreateCardUsers, Constants, CreateInbox, AddCertificate,
    Search, SearchHistory
)
from tokens import create_access_token
from datetime import datetime
from translation import translation2TM, translation2RU
import random

def read_all_users(db: Session):
    result = db.query(
        Users.id,
        Users.fullname,
        Users.phone_number,
        Users.token,
        Users.created_at,
        Users.updated_at
    ).all()
    if result:
        return result
    else:
        return False

def read_user_by_phone_number(db: Session, phone_number: str):
    result = db.query(
        Users.id,
        Users.fullname,
        Users.phone_number,
        Users.token
    ).filter(Users.phone_number == phone_number).first()
    if result:
        return result
    else:
        return False

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
    if result:
        return True
    else:
        return False
    
    
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
    if result:
        return result
    else:
        return False

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
    if result:
        return result
    else:
        return False

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
    if result:
        return result
    else:
        return False
                
def read_ads(db: Session):
    result = db.query(
        Ads.id,
        Ads.name,
        Ads.comment_of_admin,
        Ads.image,
        Ads.profile_id,
        Ads.is_main
    ).filter(Ads.is_main == True).all()
    if result:
        return result
    else:
        return False

def read_categories_by_ads(db: Session, ads_id):
    result = db.query(
        Categories.name
    ).join(JoinCategoryAds, and_(JoinCategoryAds.category_id == Categories.id, JoinCategoryAds.ads_id == ads_id)).\
        all()
    if result:
        return result
    else:
        return False

def read_category(db: Session):
    result = db.query(
        Categories.id,
        Categories.name
    ).all()
    if result:
        return result
    else:
        return False


def read_profile(db: Session, req: GetProfile):
    if req.sort == 0:
        sorting = asc(Profiles.updated_at)
    else:
        sorting = desc(Profiles.updated_at)
    result = db.query(
        Profiles.id,
        Profiles.nameTM,
        Profiles.nameRU,
        Profiles.short_descTM,
        Profiles.short_descRU,
        Profiles.like,
        Profiles.dislike,
        Profiles.instagram,
        Profiles.site,
        Profiles.status,
        Images.small_image,
        Images.large_image,
        PhoneNumbers.phone_number
    )
    result = result.join(Images, Images.profile_id == Profiles.id)
    result = result.join(PhoneNumbers, PhoneNumbers.profile_id == Profiles.id)
    result = result.join(TagProducts, TagProducts.profile_id == Profiles.id)
    result = result.join(Categories, Categories.id == Profiles.category_id)
    result = result.filter(or_(TagProducts.tags_id == elem for elem in req.tags_id))
    result = result.filter(or_(Categories.id == elem for elem in req.category))
    result = result.order_by(sorting)
    result = result.order_by(desc(Profiles.status))
    if result:
        return result.all()
    else:
        return False

def read_promotion_by_profile_id(db: Session, profile_id):
    get_promotion = db.query(
        PromotionStatuses.id,
        PromotionStatuses.promotion_status,
        PromotionStatuses.profile_id
    ).filter(PromotionStatuses.profile_id == profile_id)
    if get_promotion:
        return get_promotion.first()
    else:
        return False
    
def read_ads_by_category_id(db: Session, req: GetProfile):
    result = db.query(
        Ads.id,
        Ads.name,
        Ads.comment_of_admin,
        Ads.image,
        Ads.profile_id,
        Ads.is_main
    )
    result = result.join(JoinCategoryAds, JoinCategoryAds.ads_id == Ads.id)
    result = result.join(Categories, Categories.id == JoinCategoryAds.category_id)
    result = result.filter(or_(Categories.id == elem for elem in req.category))
    if result:
        return result.all()
    else:
        return False
        
def read_profile_by_profile_id(db: Session, profile_id):
    result = db.query(
        Profiles.id,
        Profiles.nameTM,
        Profiles.nameRU,
        Profiles.short_descTM,
        Profiles.short_descRU,
        Profiles.like,
        Profiles.dislike,
        Profiles.instagram,
        Profiles.site,
        Profiles.location,
        Profiles.address,
        Profiles.work_hours,
        Profiles.delivery,
        Profiles.cousineTM,
        Profiles.cousineRU,
        Profiles.average_check,
        Profiles.is_active_card,
        Profiles.tm_muse_card,
        Profiles.is_certificate,
        Profiles.is_promo,
        Profiles.status,
        Profiles.category_id,
        Profiles.view_count,
        Profiles.promo_count,
        Profiles.descriptionTM,
        Profiles.descriptionRU,
        Profiles.order_in_list,
        Profiles.free_time,
        Profiles.is_cash,
        Profiles.is_terminal
    ).filter(Profiles.id == profile_id)
    if result:
        return result.first()
    else:
        return False
    
def read_phone_numbers_by_profile_id(db: Session, profile_id):
    result = db.query(
        PhoneNumbers.id,
        PhoneNumbers.phone_number,
        PhoneNumbers.profile_id
    ).filter(PhoneNumbers.profile_id == profile_id)
    if result:
        return result.all()
    else:
        return False
    
def read_images_by_profile_id(db: Session, profile_id):
    result = db.query(
        Images.id,
        Images.small_image,
        Images.large_image,
        Images.isVR,
        Images.profile_id
    ).filter(Images.profile_id == profile_id)
    if result:
        return result.all()
    else:
        return False
    

def read_galleries_by_profile_id(db: Session, profile_id):
    result = db.query(
        Galleries.id,
        Galleries.medium_image,
        Galleries.large_image,
        Galleries.profile_id
    ).filter(Galleries.profile_id == profile_id)
    if result:
        return result.all()
    else:
        return False
    
def read_posts_by_profile_id(db: Session, profile_id):
    result = db.query(
        Posts.id,
        Posts.titleTM,
        Posts.titleRU,
        Posts.image,
        Posts.promotion,
        Posts.profile_id
    ).filter(Posts.profile_id == profile_id)
    if result:
        return result.all()
    else:
        return False
    
def read_certificates_by_profile_id(db: Session, profile_id):
    result = db.query(
        Certificates.id,
        Certificates.amount,
        Certificates.status,
        Certificates.user_id,
        Certificates.profile_id
    ).filter(Certificates.profile_id == profile_id)
    if result:
        return result.all()
    else:
        return False
    
def read_promo_codes_by_profile_id(db: Session, profile_id):
    result = db.query(
        PromoCodes.id,
        PromoCodes.promo_code,
        PromoCodes.status,
        PromoCodes.user_id,
        PromoCodes.profile_id
    ).filter(PromoCodes.profile_id == profile_id)
    if result:
        return result.all()
    else:
        return False

    
def read_tags_by_profile_id(db: Session, profile_id):
    result = db.query(
        Tags.id,
        Tags.tagTM,
        Tags.tagRU,
        Tags.category_id
    )
    result = result.join(TagProducts, TagProducts.tags_id == Tags.id)
    result = result.join(Profiles, Profiles.id == TagProducts.profile_id)
    result = result.filter(Profiles.id == profile_id)
    if result:
        return result.all()
    else:
        return False
    
def read_category_by_profile_id(db: Session, profile_id):
    result = db.query(
        Categories.id,
        Categories.name
    )
    result = result.join(Profiles, Profiles.category_id == Categories.id)
    result = result.filter(Profiles.id == profile_id)
    if result:
        return result.all()
    else:
        return False
    
def read_ads_by_join_category_id(db: Session, profile_id):
    result = db.query(
        Ads.id,
        Ads.nameTM,
        Ads.nameRU,
        Ads.comment_of_admin,
        Ads.image,
        Ads.profile_id,
        Ads.is_main
    )
    result = result.join(JoinCategoryAds, JoinCategoryAds.ads_id == Ads.id)
    result = result.join(Categories, Categories.id == JoinCategoryAds.category_id)
    result = result.join(Profiles, Profiles.category_id == Categories.id)
    result = result.filter(Profiles.id == profile_id)
    if result:
        return result.all()
    else:
        return False
    
def read_user_by_fullname_and_phone_number(db: Session, fullname, phone_number):
    result = db.query(
        Users.id
    ).filter(and_(Users.fullname == fullname, Users.phone_number == phone_number)).first()
    if result:
        return result
    else:
        return False

def read_inbox_by_user_id(db: Session, user_id):
    result = db.query(
        SendUser.is_read,
        Inbox.title,
        Inbox.message,
        Inbox.is_all
    )
    result = result.join(Inbox, Inbox.id == SendUser.inbox_id)
    result = result.filter(SendUser.user_id == user_id)
    if result:
        return result.all()
    else:
        return False
    
def read_inbox(db: Session):
    result = db.query(
        Inbox.id,
        Inbox.title,
        Inbox.message,
    ).filter(Inbox.is_all == True)
    if result:
        return result.all()
    else:
        return False
    
def read_answered_messages_by_user_id(db: Session, user_id):
    result = db.query(
        AnsweredMessages.title,
        AnsweredMessages.message
    )
    result = result.join(Answers, Answers.answered_msg_id == AnsweredMessages.id)
    result = result.join(Inbox, Inbox.id == Answers.inbox_id)
    result = result.join(SendUser, SendUser.inbox_id == Inbox.id)
    result = result.filter(SendUser.user_id == user_id)
    if result:
        return result.all()
    else:
        return False
    
def read_all_jobs(db: Session):
    result = db.query(
        Jobs.nameTM,
        Jobs.nameRU
    ).all()
    if result:
        return result
    else:
        return False
    
def read_profile_card_promotion(db: Session, limit, page):
    result = db.query(
        Profiles.id,
        Profiles.nameTM,
        Profiles.nameRU,
        Profiles.short_descTM,
        Profiles.short_descRU,
        Profiles.tm_muse_card,
        Profiles.like,
        Profiles.dislike,
        Profiles.instagram,
        Profiles.site,
        Images.small_image,
        Images.large_image,
        PhoneNumbers.phone_number
    )
    result = result.join(Images, Images.profile_id == Profiles.id)
    result = result.join(PhoneNumbers, PhoneNumbers.profile_id == Profiles.id)
    result = result.filter(Profiles.is_active_card == True)
    result = result.order_by(desc(Profiles.updated_at))
    result = result.offset(limit * (page - 1)).limit(limit).all()
    if result:
        return result
    else:
        return False
    
def create_card_user(db: Session, req: CreateCardUsers, userID):
    cardID = random.randrange(1000000000, 9999999999)
    cardID = str(cardID)
    str2date = datetime.strptime(req.date, '%d/%m/%y')
    new_add = CardUsers(
        date_of_birth = str2date,
        gender        = req.gender,
        passport_info = req.passport_info,
        email         = req.email,
        is_sms        = req.is_sms,
        status        = req.status,
        card_id       = cardID,
        user_id       = userID,
        job_id        = req.job_id
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    if new_add:
        return True
    else:
        return False
    
def read_constant_by_type(db: Session, type):
    result = db.query(
        Constants.id,
        Constants.titleTM,
        Constants.titleRU,
        Constants.contentTM,
        Constants.contentRU
    ).filter(Constants.type == type).all()
    if result:
        return result
    else:
        return False
    
def create_inbox(db: Session, req: CreateInbox):
    new_add = Inbox(
        title   = req.title,
        message = req.message,
        is_all  = False
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    if new_add:
        return True
    else:
        return False
    
def read_inbox_by_title_and_message(db: Session, title, message):
    result = db.query(Inbox.id).filter(and_(Inbox.title == title, Inbox.message == message)).first()
    if result:
        return result
    else:
        return False
    
def create_send_user(db: Session, userID, inboxID):
    new_add = SendUser(
        is_read     = False,
        user_id     = userID,
        inbox_id    = inboxID
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    if new_add:
        return True
    else:
        return False
    
    
def read_profile_by_profile_id_filter_is_promo(db: Session, profile_id):
    result = db.query(
        Profiles.id
    ).filter(Profiles.is_promo == True).all()
    if result:
        return True
    else:
        return False
    
def read_promo_codes_by_profile_id_user_id(db: Session, user_id, profile_id):
    result = db.query(
        PromoCodes.promo_code
    ).filter(
        and_(
            PromoCodes.user_id == user_id, 
            PromoCodes.profile_id == profile_id, 
            PromoCodes.status == 1
        ))
    if result:
        return result.all()
    else:
        return False
    
def read_promo_code_count_by_profile_id(db: Session, profile_id):
    result = db.query(
        PromoCodes
    ).filter(
        and_(
            PromoCodes.profile_id == profile_id, 
            PromoCodes.status == 1
        )).count()
    if result:
        return result
    else:
        return False


def read_profile_promo_count_by_profile_id(db: Session, profile_id):
    result = db.query(
        Profiles.promo_count
    ).filter(Profiles.id == profile_id).first()
    if result:
        return result
    else:
        return False
    
    
def create_promo_code(db: Session, profileID, userID):
    generated_promo_code = random.randrange(10000000, 99999999)
    new_add = PromoCodes(
        promo_code = generated_promo_code,
        profile_id = profileID,
        user_id    = userID,
        status     = 1
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    if new_add:
        return True
    else:
        return False
    
def create_certificates(db: Session, req: AddCertificate, userID):
    new_add = Certificates(
        amount     = req.amount,
        profile_id = req.profile_id,
        user_id    = userID,
        status     = 0
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    if new_add:
        return True
    else:
        return False
    
def create_inbox_by_certificates(db: Session, req: AddCertificate, userID):
    txt = f"amount={req.amount},profile_id={req.profile_id},user_id={userID}"
    new_add = Inbox(
        title   = "certificate",
        message = txt,
        is_all  = False,
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    if new_add:
        return txt
    else:
        return False
    
def read_inbox_by_message(db: Session, txt):
    result = db.query(
        Inbox.id
    ).filter(Inbox.message == txt).first()
    if result:
        return result
    else:
        return False
    
def create_send_user(db: Session, userID, inboxID):
    new_add = SendUser(
        user_id     = userID,
        inbox_id    = inboxID,
        is_read     = False
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    if new_add:
        return True
    else:
        return False
    
    
def search_profile_by_like(db: Session, req: Search):
    result = db.query(
        Profiles.id,
        Profiles.nameTM,
        Profiles.nameRU,
        Profiles.short_descTM,
        Profiles.short_descRU,
        Profiles.like,
        Profiles.dislike,
        Profiles.instagram,
        Profiles.site,
        Profiles.status,
        Images.small_image,
        Images.large_image,
        PhoneNumbers.phone_number
    )
    result = result.join(Images, Images.profile_id == Profiles.id)
    result = result.join(PhoneNumbers, PhoneNumbers.profile_id == Profiles.id)
    result = result.join(TagProducts, TagProducts.profile_id == Profiles.id)
    result = result.join(Categories, Categories.id == Profiles.category_id)
    result = result.filter(
        or_(
            Profiles.nameTM.like(f"%{req.text}%"),
            Profiles.nameTM.like(f"%{(req.text).translate(translation2TM)}%"),
            Profiles.nameRU.like(f"%{req.text}%"),
            Profiles.nameRU.like(f"%{(req.text).translate(translation2RU)}%")
            ))
    if result:
        return result.all()
    else:
        return False
    
def create_search_history(db: Session, txt):
    result = db.query(SearchHistory.text).filter(SearchHistory.text == txt).all()
    if result:
        db.query(SearchHistory).filter(SearchHistory.text == txt).\
            update({
                SearchHistory.count : SearchHistory.count + 1
            }, synchronize_session=False)
        db.commit()
    else:
        new_add = SearchHistory(
            text     = txt,
            count    = 1
        )
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
    return True

def read_search_history(db: Session, txt):
    result = db.query(
        SearchHistory.text,
    ).filter(SearchHistory.text == txt).order_by(desc(SearchHistory.count)).all()
    if result:
        return result
    else:
        return False