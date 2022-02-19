from imp import get_tag
from fastapi import Request
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc, func
from models import (
    Users, CodeVerify, InterestItems, Interests, UserInterests, Banners, 
    Categories, PhoneNumbers, PromotionStatuses, Images, Profiles, Ads, 
    JoinCategoryAds, GetProfile, Tags, TagProducts, Galleries, Posts,
    Certificates, PromoCodes, Inbox, SendUser, Answers, AnsweredMessages,
    CardUsers, CreateCardUsers, Constants, CreateInbox, AddCertificate,
    Search, SearchHistory, NumberSocket, PhoneVerify, Ticket_insert_schema,
    TicketBron
)
from tokens import create_access_token, check_token, decode_token
from datetime import datetime
from translation import translation2TM, translation2RU
import random
from datetime import datetime

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
        return None

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
        return None

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
        return None
    
    
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
        return result
    else:
        return None
    
    
def create_user_interest_item(db: Session, user_id, item_id):
    new_add = UserInterests(user_id = user_id, interest_item_id = item_id)
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    if new_add:
        return True
    else:
        return None
    
def delete_user_interest(db: Session, user_id):
    delete = db.query(UserInterests).filter(UserInterests.user_id == user_id).\
        delete(synchronize_session=None)
    db.commit()
    if delete:
        return True
    else:
        return None
    
def read_banner(db: Session):
    result = db.query(
        Banners.id,
        Banners.image,
        Banners.order,
        Banners.link,
        Banners.profile_id
    ).order_by(desc(Banners.order)).all()
    if result:
        return result
    else:
        return None

def read_movies(db: Session):
    result = db.query(
        Profiles.id,
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
        return None

def read_promotions(db: Session, page):

    result = db.query(
        Posts.id,
        Posts.titleTM,
        Posts.titleRU,
        Posts.descriptionTM,
        Posts.descriptionRU,
        Posts.comment_of_admin,
        Posts.status,
        Posts.image,
        Posts.promotion,
        Posts.view_count,
        Posts.like,
        Posts.dislike,
        Posts.profile_id,
        Profiles.instagram,
    )
    result = result.join(Profiles, Profiles.id == Posts.profile_id)
    result = result.offset(20 * (page-1)).limit(20).all()
    new_list = []
    for res in result:
        res_dict = dict(res)
        phone_numbers = read_phone_numbers_by_profile_id(db=db, profile_id=res.profile_id)
        res_dict["numbers"] = list(phone_numbers)
        new_list.append(res_dict)
    result = new_list
    if result:
        return result
    else:
        return None
                
def read_ads(db: Session):
    result = db.query(
        Ads.id,
        Ads.nameTM,
        Ads.nameRU,
        Ads.comment_of_admin,
        Ads.image,
        Ads.profile_id,
        Ads.is_main
    ).filter(Ads.is_main == True).all()
    if result:
        return result
    else:
        return None

def read_categories_by_ads(db: Session, ads_id):
    result = db.query(
        Categories.name
    ).join(JoinCategoryAds, and_(JoinCategoryAds.category_id == Categories.id, JoinCategoryAds.ads_id == ads_id)).\
        all()
    if result:
        return result
    else:
        return None

def read_category(db: Session):
    result = db.query(
        Categories.id,
        Categories.name
    ).all()
    if result:
        return result
    else:
        return None


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
        Profiles.is_VIP,
        Profiles.category_id,
        Profiles.WiFi
    )
    if len(req.tags_id) > 0:
        result = result.join(TagProducts, TagProducts.profile_id == Profiles.id)
        result = result.filter(or_(TagProducts.tags_id == elem for elem in req.tags_id))
    if len(req.category) > 0:
        result = result.join(Categories, Categories.id == Profiles.category_id)
        result = result.filter(or_(Categories.id == elem for elem in req.category))
    result = result.filter(Profiles.status != 0)
    result = result.order_by(sorting)
    result = result.order_by(desc(Profiles.is_VIP))
    result = result.offset(req.limit * (req.page - 1)).limit(req.limit)
    result = result.distinct().all()
    new_list = []
    for res in result:
        res = dict(res)
        get_images = read_images_by_profile_id_isVR_false(db=db, profile_id=res["id"])
        get_phone_number = read_phone_numbers_by_profile_id(db=db, profile_id=res["id"])
        if get_images:
            res["image"] = get_images
        if get_phone_number:
            res["phone_numbers"] = get_phone_number
        new_list.append(res)
    result = new_list
    result = sorted(result, key=lambda d: d["is_VIP"], reverse=True)
    if result:
        return result
    else:
        return None

def read_promotion_by_profile_id(db: Session, profile_id):
    get_promotion = db.query(
        PromotionStatuses.id,
        PromotionStatuses.promotion_status,
        PromotionStatuses.profile_id
    ).filter(PromotionStatuses.profile_id == profile_id).first()
    if get_promotion:
        return get_promotion
    else:
        return None
    
def read_ads_random(db: Session):
    result = db.query(
        Ads.id,
        Ads.nameTM,
        Ads.nameRU,
        Ads.comment_of_admin,
        Ads.image,
        Ads.profile_id,
        Ads.is_main,
        Ads.site_url
    )
    result = result.filter(Ads.is_main == None)
    result = result.order_by(func.random())
    if result:
        return result.all()
    else:
        return None
        
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
    ).filter(Profiles.id == profile_id).first()
    if result:
        return result
    else:
        return None
    
def read_phone_numbers_by_profile_id(db: Session, profile_id):
    result = db.query(
        PhoneNumbers.id,
        PhoneNumbers.phone_number,
    ).filter(PhoneNumbers.profile_id == profile_id)
    if result:
        return result.all()
    else:
        return None
    
def read_images_by_profile_id(db: Session, profile_id):
    result = db.query(
        Images.id,
        Images.small_image,
        Images.large_image,
        Images.isVR,
    ).filter(Images.profile_id == profile_id)
    if result:
        return result.all()
    else:
        return None
    

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
        return None
    
def read_posts_by_profile_id(db: Session, profile_id):
    result = db.query(
        Posts.id,
        Posts.titleTM,
        Posts.titleRU,
        Posts.image,
        Posts.promotion,
        Posts.profile_id,
        Posts.descriptionTM,
        Posts.descriptionRU,
        Posts.comment_of_admin,
        Posts.status,
        Posts.view_count,
        Posts.like,
        Posts.dislike
    ).filter(Posts.profile_id == profile_id)
    if result:
        return result.all()
    else:
        return None
    
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
        return None
    
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
        return None

    
def read_tags_by_profile_id(db: Session, profile_id):
    result = db.query(
        Tags.id,
        Tags.tagTM,
        Tags.tagRU,
        Tags.category_id
    )
    result = result.join(TagProducts, TagProducts.tags_id == Tags.id)
    result = result.join(Profiles, Profiles.id == TagProducts.profile_id)
    result = result.filter(Profiles.id == profile_id).all()
    if result:
        return result
    else:
        return None
    
def read_tags_by_category_id(db: Session, category_id):
    result = db.query(
        Tags.id,
        Tags.tagTM,
        Tags.tagRU
    ).filter(Tags.category_id == category_id).all()
    if result:
        return result
    else:
        return []
    
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
        return None
    
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
    result = result.filter(Ads.profile_id == profile_id)
    if result:
        return result.all()
    else:
        return None
    
def read_user_by_fullname_and_phone_number(db: Session, fullname, phone_number):
    result = db.query(
        Users.id
    ).filter(and_(Users.fullname == fullname, Users.phone_number == phone_number)).first()
    if result:
        return result
    else:
        return None

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
        return None
    
def read_inbox(db: Session):
    result = db.query(
        Inbox.id,
        Inbox.title,
        Inbox.message,
    ).filter(Inbox.is_all == True)
    if result:
        return result.all()
    else:
        return None
    
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
        return None

    
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
        Profiles.site
    )
    result = result.filter(Profiles.tm_muse_card > 0)
    result = result.order_by(desc(Profiles.updated_at))
    result = result.offset(limit * (page - 1)).limit(limit).all()
    new_list = []
    for res in result:
        res = dict(res)
        get_images = read_images_by_profile_id(db=db, profile_id=res["id"])
        get_images_vr = read_images_by_profile_id_isVR_false(db=db, profile_id=res["id"])
        get_phone_number = read_phone_numbers_by_profile_id(db=db, profile_id=res["id"])
        if get_images:
            res["images"] = get_images
        if get_images_vr:
            res["image_vr"] = get_images_vr
        if get_phone_number:
            res["phone_numbers"] = get_phone_number
        new_list.append(res)
    result = new_list
    if result:
        return result
    else:
        return None
    
def create_card_user(db: Session, req: CreateCardUsers, userID):
    cardID = random.randrange(1000000000, 9999999999)
    cardID = str(cardID)
    str2date = datetime.strptime(req.date, '%d/%m/%Y')
    new_add = CardUsers(
        date_of_birth = str2date,
        gender        = req.gender,
        email         = req.email,
        is_sms        = req.is_sms,
        status        = req.status,
        card_id       = cardID,
        user_id       = userID,
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    if new_add:
        return True
    else:
        return None
    
def read_constant_by_type(db: Session, type):
    result = db.query(
        Constants.id,
        Constants.titleTM,
        Constants.titleRU,
        Constants.contentTM,
        Constants.contentRU,
        Constants.contentTM_dark,
        Constants.contentRU_dark
    ).filter(Constants.type == type).all()
    if result:
        return result
    else:
        return None
    
def create_inbox(db: Session, req: CreateInbox):
    new_add = Inbox(
        title   = req.title,
        message = req.message,
        is_all  = None
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    if new_add:
        return True
    else:
        return None
    
def read_inbox_by_title_and_message(db: Session, title, message):
    result = db.query(Inbox.id).filter(and_(Inbox.title == title, Inbox.message == message)).first()
    if result:
        return result
    else:
        return None
    
def create_send_user(db: Session, userID, inboxID):
    new_add = SendUser(
        is_read     = None,
        user_id     = userID,
        inbox_id    = inboxID
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    if new_add:
        return True
    else:
        return None
    
    
def read_profile_by_profile_id_filter_is_promo(db: Session, profile_id):
    result = db.query(
        Profiles.is_promo
    ).filter(Profiles.id == profile_id).first()
    if result.is_promo:
        return True
    else:
        return None
    
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
        return None
    
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
        return None


def read_profile_promo_count_by_profile_id(db: Session, profile_id):
    result = db.query(
        Profiles.promo_count
    ).filter(Profiles.id == profile_id).first()
    if result:
        return result
    else:
        return None
    
    
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
        return generated_promo_code
    else:
        return None
    
def create_certificates(db: Session, req: AddCertificate, userID):
    get_profile = db.query(
        Profiles.is_certificate
    ).filter(Profiles.id == req.profile_id).first()
    if not get_profile.is_certificate:
        return None
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
        return None
    
def create_inbox_by_certificates(db: Session, req: AddCertificate, userID):
    txt = f"amount={req.amount},profile_id={req.profile_id},user_id={userID}"
    new_add = Inbox(
        title   = "certificate",
        message = txt,
        is_all  = None,
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    if new_add:
        return txt
    else:
        return None
    
def read_inbox_by_message(db: Session, txt):
    result = db.query(
        Inbox.id
    ).filter(Inbox.message == txt).first()
    if result:
        return result
    else:
        return None
    
def create_send_user(db: Session, userID, inboxID):
    new_add = SendUser(
        user_id     = userID,
        inbox_id    = inboxID,
        is_read     = None
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    if new_add:
        return True
    else:
        return None
    
    
def search_profile_by_like(db: Session, req: Search, page, limit):
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
    )
    result = result.filter(
        or_(
            func.lower(Profiles.nameTM).like(f"%{req.text}%"),
            func.lower(Profiles.nameTM).like(f"%{(req.text).translate(translation2TM)}%"),
            func.lower(Profiles.nameRU).like(f"%{req.text}%"),
            func.lower(Profiles.nameRU).like(f"%{(req.text).translate(translation2RU)}%")
            ))
    result = result.offset(20 * (page-1)).limit(limit).all()
    new_list = []
    for res in result:
        res = dict(res)
        get_images = read_images_by_profile_id_isVR_false(db=db, profile_id=res["id"])
        get_phone_number = read_phone_numbers_by_profile_id(db=db, profile_id=res["id"])
        if get_images:
            res["image"] = get_images
        if get_phone_number:
            res["phone_numbers"] = get_phone_number
        new_list.append(res)
    result = new_list
    if result:
        return result
    else:
        return None
    
def create_search_history(db: Session, txt):
    result = db.query(SearchHistory.text).filter(SearchHistory.text == txt).all()
    if result:
        db.query(SearchHistory).filter(SearchHistory.text == txt).\
            update({
                SearchHistory.count : SearchHistory.count + 1
            }, synchronize_session=None)
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

def read_search_history(db: Session):
    result = db.query(
        SearchHistory.text,
    ).order_by(desc(SearchHistory.count)).limit(20).all()
    if result:
        return result
    else:
        return None
    
    
def create_number_socket(db: Session, number: PhoneVerify, code):
    new_add = NumberSocket(
        phone_number = number.phone_number,
        code         = code,
        created_at   = datetime.now(),
        updated_at   = datetime.now()
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    if new_add:
        return True
    else:
        return None
    
    
def read_phone_number_and_code(db: Session, phone_number, code):
    result = db.query(
        NumberSocket.phone_number,
        NumberSocket.code,
        NumberSocket.created_at
    )\
    .filter(and_(NumberSocket.phone_number == phone_number, NumberSocket.code == code))\
    .first()
    if result:
        return result
    else:
        return None
    
def delete_number_socket(db: Session, phone_number):
    new_delete = db.query(NumberSocket)\
    .filter(NumberSocket.phone_number == phone_number)\
    .delete(synchronize_session=None)
    db.commit()
    if new_delete:
        return True
    else:
        return None
    
    
def read_user_id_from_token(db: Session, header_param: Request):
    token = check_token(header_param=header_param)
    payload = decode_token(token=token)
    if not payload:
        return None
    phone_number: str = payload.get("phone_number")
    result = read_user_by_phone_number(db=db, phone_number=phone_number)
    if result:
        return result.id
    else:
        return None
    
    
def read_interest_items_by_user_id(db: Session, user_id):
    result = db.query(
        InterestItems.id,
        InterestItems.titleTM,
        InterestItems.titleRU,
        InterestItems.interest_id
    )
    result = result.join(UserInterests, UserInterests.interest_item_id == InterestItems.id)
    result = result.filter(UserInterests.user_id == user_id).all()
    if result:
        return result
    else:
        return None
    
    
def read_images_by_profile_id_isVR_false(db: Session, profile_id):
    result = db.query(
        Images.id,
        Images.small_image,
        Images.large_image,
        Images.isVR
    )
    result = result.filter(Images.profile_id == profile_id)
    result = result.filter(Images.isVR == False)
    if result:
        return result.first()
    else:
        return None
    
    
async def create_ticket(db: Session, ticket: Ticket_insert_schema):
    date_string = datetime.strptime(ticket.movie_date, "%d/%m/%Y")
    time_string = datetime.strptime(ticket.movie_time, "%H:%M")
    new_add = TicketBron(
        cinema_id       = ticket.cinema_id,
        profile_id      = ticket.profile_id,
        user_id         = ticket.user_id,
        movie_date      = date_string,
        movie_time      = time_string,
        ticket_count    = ticket.ticket_count,
        ticket_price    = ticket.ticket_price,
        ticket_discount = ticket.ticket_discount,
        status          = 1
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    if new_add:
        return new_add.id
    else:
        return None
    
    
async def read_current_ticket(db: Session, user_id):
    result = db.query(
        TicketBron.id,
        TicketBron.profile_id,
        TicketBron.movie_date,
        TicketBron.movie_time,
        TicketBron.ticket_count,
        TicketBron.ticket_discount,
        TicketBron.ticket_price,
        Profiles.nameTM,
        Profiles.nameRU,
        Profiles.short_descTM,
        Profiles.short_descRU,
        Profiles.descriptionTM,
        Profiles.descriptionRU,
        Users.fullname,
        Users.phone_number
    )
    result = result.join(Profiles, Profiles.id == TicketBron.profile_id)
    result = result.join(Users, Users.id == TicketBron.user_id)
    result = result.filter(TicketBron.user_id == user_id).all()
    for res in result:
        res = dict(res)
        image = read_images_by_profile_id_isVR_false(db=db, profile_id=res["profile_id"])
        if image:
            res["image"] = image
    if result:
        return result
    else:
        return None