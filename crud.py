from fastapi import Request
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc, func
from models import (
    Users, CodeVerify, InterestItems, Interests, UserInterests, Banners, 
    Categories, PhoneNumbers, Images, Profiles, Ads, 
    JoinCategoryAds, GetProfile, Tags, Galleries, Posts, Certificates, 
    PromoCodes, Inbox, SendUser, Answers, AnsweredMessages, CardUsers, 
    CreateCardUsers, Constants, CreateInbox, AddCertificate, Search, 
    SearchHistory, NumberSocket, PhoneVerify, Ticket_insert_schema,
    TicketBron, ProfileView, AdsView, Ads2Profile_count, ViewCountSchema,
    AppVisitors, LikeDislikeSchema, SendUserIsReadSchema, TicketStatusUpdateSchema,
    Admin
)
from models.models import PopUp
from tokens import create_access_token, check_token, decode_token
from datetime import datetime
from translation import translation2TM, translation2RU
import random
from datetime import datetime

async def read_all_users(db: Session):
    result = db.query(
        Users.id,
        Users.fullname,
        Users.phone_number,
        Users.token,
        Users.created_at,
        Users.updated_at
    ).all()
    db.close()
    if result:
        return result
    else:
        return None

async def read_user_by_phone_number(db: Session, phone_number: str):
    result = db.query(
        Users.id,
        Users.fullname,
        Users.phone_number,
        Users.token
    ).filter(Users.phone_number == phone_number).first()
    db.close()
    if result:
        return result
    else:
        return None

async def create_user(db: Session, req: CodeVerify):
    newDict = {
        "fullname"      : req.fullname,
        "phone_number"  : req.phone_number
    }
    access_token = await create_access_token(newDict)
    new_add = Users(
        fullname     = req.fullname,
        phone_number = req.phone_number,
        token        = access_token
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    if new_add:
        return True
    else:
        return None
    
    
async def read_interests(db: Session):
    result = db.query(
        Interests.id,
        Interests.titleTM,
        Interests.titleRU
    ).all()
    db.close()
    return result

async def read_interest_items_by_interest_id(db: Session, interest_id):
    result = db.query(
        InterestItems.id,
        InterestItems.titleTM,
        InterestItems.titleRU
    ).filter(InterestItems.interest_id == interest_id).all()
    db.close()
    if result:
        return result
    else:
        return None
    
    
async def create_user_interest_item(db: Session, user_id, item_id):
    new_add = UserInterests(
        user_id = user_id, 
        interest_item_id = item_id
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    if new_add:
        return True
    else:
        return None
    
# async def delete_user_interest(db: Session, user_id):
#     get_user_interest = await db.query(UserInterests.interest_item_id).filter(UserInterests.user_id == user_id).all()
#     if get_user_interest:
#         for interest in get_user_interest:
#             await db.query(InterestItems).filter(InterestItems.id == interest.interest_item_id)\
#                 .delete(synchronize_session=False)
#             db.commit()
#     delete = await db.query(UserInterests.interest_item_id).filter(UserInterests.user_id == user_id)\
#         .delete(synchronize_session=False)
#     db.commit()
#     if delete:
#         return True
#     else:
#         return None
    
async def read_banner(db: Session):
    result = db.query(
        Banners.id,
        Banners.image,
        Banners.order,
        Banners.link,
        Banners.profile_id
    ).order_by(desc(Banners.order)).all()
    db.close()
    if result:
        return result
    else:
        return None

async def read_movies(db: Session):
    result = db.query(
        Profiles.id,
        Profiles.nameTM,
        Profiles.nameRU,
        Profiles.short_descTM,
        Profiles.short_descRU,
        Profiles.created_at,
        Profiles.updated_at
    ).filter(and_(Profiles.category_id == 2, Profiles.status != 0))\
        .order_by(desc(Profiles.created_at)).limit(20).all()
    db.close()
    new_list = []
    for res in result:
        res = dict(res)
        image = await read_images_by_profile_id_isVR_false(db=db, profile_id=res["id"])
        if image:
            res["image"] = image
        new_list.append(res)
    result = new_list
    if result:
        return result
    else:
        return None

async def read_promotions(db: Session, page):

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
        Posts.created_at,
        Posts.updated_at,
        Profiles.instagram,
    )
    result = result.join(Profiles, Profiles.id == Posts.profile_id)
    result = result.order_by(desc(Posts.updated_at))
    result = result.offset(8 * (page-1)).limit(8).all()
    db.close()
    new_list = []
    for res in result:
        res_dict = dict(res)
        phone_numbers = await read_phone_numbers_by_profile_id(db=db, profile_id=res.profile_id)
        res_dict["numbers"] = phone_numbers
        new_list.append(res_dict)
    result = new_list
    if result:
        return result
    else:
        return None
                
async def read_ads(db: Session):
    result = db.query(
        Ads.id,
        Ads.nameTM,
        Ads.nameRU,
        Ads.comment_of_admin,
        Ads.image,
        Ads.site_url,
        Ads.profile_id,
        Ads.is_main
    ).filter(Ads.is_main == True).all()
    db.close()
    if result:
        return result
    else:
        return None

def read_categories_by_ads(db: Session, ads_id):
    result = db.query(
        Categories.name
    ).join(JoinCategoryAds, and_(JoinCategoryAds.category_id == Categories.id, JoinCategoryAds.ads_id == ads_id)).\
        all()
    db.close()
    if result:
        return result
    else:
        return None

async def read_category(db: Session):
    result = db.query(
        Categories.id,
        Categories.name
    ).all()
    db.close()
    if result:
        return result
    else:
        return None


async def read_profile(db: Session, req: GetProfile):
    if req.sort == 1:
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
        Profiles.WiFi,
        Profiles.average_check,
        Profiles.own_promotion
    )
    if len(req.tags_id) > 0:
        result = result.join(Tags, Tags.profile_id == Profiles.id)
        result = result.filter(or_(Tags.id == elem for elem in req.tags_id))
    if len(req.category) > 0:
        result = result.join(Categories, Categories.id == Profiles.category_id)
        result = result.filter(or_(Categories.id == elem for elem in req.category))
    result = result.filter(Profiles.status != 0)
    result = result.order_by(desc(Profiles.is_VIP))
    result = result.order_by(sorting)
    result = result.offset(req.limit * (req.page - 1)).limit(req.limit)
    result = result.distinct().all()
    db.close()
    new_list = []
    for res in result:
        res = dict(res)
        get_images = await read_images_by_profile_id_isVR_false(db=db, profile_id=res["id"])
        get_phone_number = await read_phone_numbers_by_profile_id(db=db, profile_id=res["id"])
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

    
async def read_ads_random(db: Session):
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
    result = result.filter(Ads.is_main == False)
    result = result.order_by(func.random()).all()
    db.close()
    if result:
        return result
    else:
        return None
        
async def read_profile_by_profile_id(db: Session, profile_id):
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
        Profiles.is_terminal,
        Profiles.cinema_id,
        Profiles.own_promotion,
        Profiles.WiFi,
        Profiles.required_promotion
    ).filter(Profiles.id == profile_id).first() 
    db.close()
    if result:
        return result
    else:
        return None
    
async def read_phone_numbers_by_profile_id(db: Session, profile_id):
    result = db.query(
        PhoneNumbers.id,
        PhoneNumbers.phone_number,
        PhoneNumbers.profile_id
    ).filter(PhoneNumbers.profile_id == profile_id).all()
    db.close()
    if result:
        return result
    else:
        return None
    
async def read_images_by_profile_id(db: Session, profile_id):
    result = db.query(
        Images.id,
        Images.small_image,
        Images.large_image,
        Images.isVR,
    ).filter(Images.profile_id == profile_id).all()
    db.close()
    if result:
        return result
    else:
        return None
    

async def read_galleries_by_profile_id(db: Session, profile_id):
    result = db.query(
        Galleries.id,
        Galleries.medium_image,
        Galleries.large_image,
        Galleries.profile_id
    ).filter(Galleries.profile_id == profile_id).all()
    db.close()
    if result:
        return result
    else:
        return None
    
async def read_posts_by_profile_id(db: Session, profile_id):
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
        Posts.dislike,
        Profiles.instagram
    )\
    .join(Profiles, Profiles.id == Posts.profile_id)\
    .filter(Posts.profile_id == profile_id)\
    .all()
    db.close()
    if result:
        return result
    else:
        return None
    
async def read_certificates_by_profile_id(db: Session, profile_id):
    result = db.query(
        Certificates.id,
        Certificates.amount,
        Certificates.status,
        Certificates.user_id,
        Certificates.profile_id
    ).filter(Certificates.profile_id == profile_id).all()
    db.close()
    if result:
        return result
    else:
        return None
    
async def read_promo_codes_by_profile_id(db: Session, profile_id):
    result = db.query(
        PromoCodes.id,
        PromoCodes.promo_code,
        PromoCodes.status,
        PromoCodes.user_id,
        PromoCodes.profile_id
    ).filter(PromoCodes.profile_id == profile_id).all()
    db.close()
    if result:
        return result
    else:
        return None

    
async def read_tags_by_profile_id(db: Session, profile_id):
    result = db.query(
        Tags.id,
        Tags.tagTM,
        Tags.tagRU,
        Tags.category_id
    )
    result = result.join(Profiles, Profiles.id == Tags.profile_id)
    result = result.filter(Profiles.id == profile_id).all()
    db.close()
    if result:
        return result
    else:
        return None
    
async def read_tags_by_category_id(db: Session, category_id):
    result = db.query(
        Tags.id,
        Tags.tagTM,
        Tags.tagRU
    ).filter(Tags.category_id == category_id).all()
    db.close()
    if result:
        return result
    else:
        return []
    
async def read_category_by_profile_id(db: Session, profile_id):
    result = db.query(
        Categories.id,
        Categories.name
    )
    result = result.join(Profiles, Profiles.category_id == Categories.id)
    result = result.filter(Profiles.id == profile_id).all()
    db.close()
    if result:
        return result
    else:
        return None
    
async def read_ads_by_join_category_id(db: Session, profile_id):
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
    result = result.filter(Ads.profile_id == profile_id).all()
    db.close()
    if result:
        return result
    else:
        return None
    
async def read_user_by_fullname_and_phone_number(db: Session, fullname, phone_number):
    result = db.query(
        Users.id
    ).filter(and_(Users.fullname == fullname, Users.phone_number == phone_number)).first()
    db.close()
    if result:
        return result
    else:
        return None

async def read_inbox_by_user_id(db: Session, user_id):
    result = db.query(
        Inbox.id,
        SendUser.is_read,
        Inbox.title,
        Inbox.message,
        Inbox.is_all,
        Inbox.created_at,
        Inbox.updated_at
    )
    result = result.join(Inbox, Inbox.id == SendUser.inbox_id)
    result = result.filter(SendUser.user_id == user_id)
    result = result.order_by(desc(Inbox.created_at)).all()
    db.close()
    if result:
        return result
    else:
        return None
    
async def read_inbox(db: Session):
    result = db.query(
        Inbox.id,
        Inbox.title,
        Inbox.message,
        Inbox.created_at,
        Inbox.updated_at
    ).filter(Inbox.is_all == True)\
    .order_by(desc(Inbox.created_at))\
    .all()
    db.close()
    if result:
        return result
    else:
        return None
    
async def read_answered_messages_by_user_id(db: Session, user_id):
    result = db.query(
        AnsweredMessages.title,
        AnsweredMessages.message,
        AnsweredMessages.created_at,
        AnsweredMessages.updated_at
    )
    result = result.join(Answers, Answers.answered_msg_id == AnsweredMessages.id)
    result = result.join(Inbox, Inbox.id == Answers.inbox_id)
    result = result.join(SendUser, SendUser.inbox_id == Inbox.id)
    result = result.filter(SendUser.user_id == user_id)
    result = result.order_by(desc(AnsweredMessages.created_at)).all()
    db.close()
    if result:
        return result
    else:
        return None

async def update_send_user_is_read(db: Session, id, req: SendUserIsReadSchema):
    new_update = db.query(SendUser).filter(SendUser.id == id).\
        update({
            SendUser.is_read : req.is_read
        }, synchronize_session=False)
    db.commit()
    db.close()
    if new_update:
        return True
    else:
        return None
    
    
    
async def read_profile_card_promotion(db: Session, limit, page):
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
    result = result.filter(Profiles.status != 0)
    result = result.order_by(desc(Profiles.updated_at))
    result = result.offset(limit * (page - 1)).limit(limit).all()
    db.close()
    new_list = []
    for res in result:
        res = dict(res)
        get_images = await read_images_by_profile_id(db=db, profile_id=res["id"])
        get_images_vr = await read_images_by_profile_id_isVR_false(db=db, profile_id=res["id"])
        get_phone_number = await read_phone_numbers_by_profile_id(db=db, profile_id=res["id"])
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
    
async def create_card_user(db: Session, req: CreateCardUsers, userID):
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
    db.close()
    if new_add:
        return True
    else:
        return None
    
async def read_card_user_by_user_id(db: Session, user_id):
    result = db.query(CardUsers)\
    .filter(CardUsers.user_id == user_id)\
    .all()
    db.close()
    if result:
        return True
    else:
        return False
    
async def read_constant_by_type(db: Session, type):
    result = db.query(
        Constants.id,
        Constants.titleTM,
        Constants.titleRU,
        Constants.contentTM,
        Constants.contentRU,
        Constants.contentTM_dark,
        Constants.contentRU_dark
    ).filter(Constants.type == type).all()
    db.close()
    if result:
        return result
    else:
        return None
    
async def create_inbox(db: Session, req: CreateInbox):
    new_add = Inbox(
        title   = req.title,
        message = req.message,
        is_all  = False
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    if new_add:
        return True
    else:
        return None
    
    
async def create_inbox_card(db: Session, req):
    new_add = Inbox(
        title   = req["title"],
        message = req["message"],
        is_all  = False
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    if new_add:
        return new_add
    else:
        return None
    
    
async def read_inbox_by_title_and_message(db: Session, title, message):
    result = db.query(Inbox.id).filter(and_(Inbox.title == title, Inbox.message == message)).first()
    db.close()
    if result:
        return result
    else:
        return None
    
    
async def create_send_user(db: Session, userID, inboxID):
    new_add = SendUser(
        is_read     = False,
        user_id     = userID,
        inbox_id    = inboxID
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    if new_add:
        return True
    else:
        return None
    
    
async def read_profile_by_profile_id_filter_is_promo(db: Session, profile_id):
    result = db.query(
        Profiles.is_promo
    ).filter(Profiles.id == profile_id).first()
    db.close()
    if result:
        return True
    else:
        return None
    
async def read_promo_codes_by_profile_id_user_id(db: Session, user_id, profile_id):
    result = db.query(
        PromoCodes.promo_code
    ).filter(
        and_(
            PromoCodes.user_id == user_id, 
            PromoCodes.profile_id == profile_id, 
            PromoCodes.status == 1
        )).all()
    db.close()
    if result:
        return result
    else:
        return None
    
async def read_promo_code_count_by_profile_id(db: Session, profile_id):
    result = db.query(
        PromoCodes
    ).filter(
        and_(
            PromoCodes.profile_id == profile_id, 
            PromoCodes.status == 1
        )).count()
    db.close()
    if result:
        return result
    else:
        return 0


async def read_profile_promo_count_by_profile_id(db: Session, profile_id):
    result = db.query(
        Profiles.promo_count
    ).filter(Profiles.id == profile_id).first()
    db.close()
    if result:
        return result
    else:
        return None
    
    
async def create_promo_code(db: Session, profileID, userID):
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
    db.close()
    if new_add:
        return generated_promo_code
    else:
        return None
    
async def create_certificates(db: Session, req: AddCertificate, userID):
    get_profile = db.query(
        Profiles.is_certificate
    ).filter(Profiles.id == req.profile_id).first()
    db.close()
    # if not get_profile.is_certificate:
    #     return None
    new_add = Certificates(
        amount     = req.amount,
        profile_id = req.profile_id,
        user_id    = userID,
        status     = 0
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    if new_add:
        return True
    else:
        return None
    
async def create_inbox_by_certificates(db: Session, req: AddCertificate, userID):
    profile = db.query(
        Profiles.nameTM,
        Profiles.nameRU
    )\
    .filter(Profiles.id == req.profile_id)\
    .first()
    db.close()
    user = db.query(
        Users.fullname
    )\
    .filter(Users.id == userID)\
    .first()
    db.close()
    txtTM = "Salam, {}!\nSiziň \"{}\" atly alan sertifikatyňyz üstünlikli hasaba alyndy. Adminstrasiýa tarapyndan tassyklanmagyna garaşyň.\nSertifikat möçberi: {} TMT \n\n".format(user.fullname, profile.nameTM, req.amount)
    txtRU = "Здравствуйте {}!\nВаш сертификат \"{}\" успешно зарегистрирован. Дождитесь одобрения администрации.\nСумма сертификата: {} TMT".format(user.fullname, profile.nameRU, req.amount)
    txt = txtTM + txtRU
    new_add = Inbox(
        title   = "Sertifikat / Сертификат",
        message = txt,
        is_all  = False,
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    if new_add:
        return txt
    else:
        return None
    
async def read_inbox_by_message(db: Session, txt):
    result = db.query(
        Inbox.id
    ).filter(Inbox.message == txt).first()
    db.close()
    if result:
        return result
    else:
        return None
    
    
async def search_profile_by_like(db: Session, req: Search, page, limit):
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
    db.close()
    new_list = []
    for res in result:
        res = dict(res)
        get_images = await read_images_by_profile_id_isVR_false(db=db, profile_id=res["id"])
        get_phone_number = await read_phone_numbers_by_profile_id(db=db, profile_id=res["id"])
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
    
async def create_search_history(db: Session, txt):
    result = db.query(SearchHistory.text).filter(SearchHistory.text == txt).all()
    if result:
        db.query(SearchHistory).filter(SearchHistory.text == txt).\
            update({
                SearchHistory.count : SearchHistory.count + 1
            }, synchronize_session=None)
        db.commit()
        db.close()
    else:
        new_add = SearchHistory(
            text     = txt,
            count    = 1
        )
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        db.close()
    return True

async def read_search_history(db: Session):
    result = db.query(
        SearchHistory.text,
    ).order_by(desc(SearchHistory.count)).limit(20).all()
    db.close()
    if result:
        return result
    else:
        return None
    
    
async def create_number_socket(db: Session, number: PhoneVerify, code):
    new_add = NumberSocket(
        phone_number = number.phone_number,
        code         = code,
        created_at   = datetime.now(),
        updated_at   = datetime.now()
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    if new_add:
        return True
    else:
        return None
    
    
async def read_phone_number_and_code(db: Session, phone_number, code):
    result = db.query(
        NumberSocket.phone_number,
        NumberSocket.code,
        NumberSocket.created_at
    )\
    .filter(and_(NumberSocket.phone_number == phone_number, NumberSocket.code == code))\
    .first()
    db.close()
    if result:
        return result
    else:
        return None
    
async def delete_number_socket(db: Session, phone_number):
    new_delete = db.query(NumberSocket)\
    .filter(NumberSocket.phone_number == phone_number)\
    .delete(synchronize_session=False)
    db.commit()
    db.close()
    if new_delete:
        return True
    else:
        return None
    
    
async def read_user_id_from_token(db: Session, header_param: Request):
    token = await check_token(header_param=header_param)
    payload = await decode_token(token=token)
    if not payload:
        return None
    phone_number: str = payload.get("phone_number")
    result = await read_user_by_phone_number(db=db, phone_number=phone_number)
    if result:
        return result.id
    else:
        return None
    
    
async def read_interest_items_by_user_id(db: Session, user_id):
    result = db.query(
        InterestItems.id,
        InterestItems.titleTM,
        InterestItems.titleRU,
        InterestItems.interest_id
    )
    result = result.join(UserInterests, UserInterests.interest_item_id == InterestItems.id)
    result = result.filter(UserInterests.user_id == user_id).all()
    db.close()
    if result:
        return result
    else:
        return None
    
    
async def read_images_by_profile_id_isVR_false(db: Session, profile_id):
    result = db.query(
        Images.id,
        Images.small_image,
        Images.large_image,
        Images.isVR
    )
    result = result.filter(Images.profile_id == profile_id)
    result = result.filter(Images.isVR == False).all()
    db.close()
    if result:
        return result
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
    db.close()
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
        TicketBron.status,
        Profiles.nameTM,
        Profiles.nameRU,
        Profiles.short_descTM,
        Profiles.short_descRU,
        Profiles.descriptionTM,
        Profiles.descriptionRU,
        Users.fullname,
        Users.phone_number,
        TicketBron.created_at,
        TicketBron.updated_at
    )
    result = result.join(Profiles, Profiles.id == TicketBron.profile_id)
    result = result.join(Users, Users.id == TicketBron.user_id)
    result = result.filter(TicketBron.user_id == user_id).order_by(desc(TicketBron.id)).all()
    db.close()
    new_list = []
    for res in result:
        res = dict(res)
        image = await read_images_by_profile_id_isVR_false(db=db, profile_id=res["profile_id"])
        if image:
            res["image"] = image
        new_list.append(res)
    result = new_list
    if result:
        return result
    else:
        return None
    
    
async def create_profile_view(db: Session, profile_id):
    new_add = ProfileView(
        profile_id = profile_id
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    new_update = db.query(Profiles).filter(Profiles.id == profile_id).\
        update({
            Profiles.view_count : Profiles.view_count + 1
        }, synchronize_session=False)
    db.commit()
    db.close()
    if new_add:
        return True
    else:
        return None
    
    
async def create_view_count(db: Session, view: ViewCountSchema):
    if view.type == "post":
        profile_id = db.query(Posts.profile_id).filter(Posts.id == view.ads_id).first()
        db.close()
        db.query(Posts).filter(Posts.id == view.ads_id)\
        .update({Posts.view_count : Posts.view_count + 1}, synchronize_session=False)
        db.commit()
        db.close()
    if view.type == "ads":
        profile_id = db.query(Ads.profile_id).filter(Ads.id == view.ads_id).first()
        db.close()
        
    if view.type == "banner":
        profile_id = db.query(Images.profile_id).filter(Images.id == view.ads_id).first()
        db.close()
        
    if view.type == "popup":
        profile_id = db.query(PopUp.profile_id).filter(PopUp.id == view.ads_id).first()
        db.close()
        
    new_add = AdsView(
        ads_id      = view.ads_id,
        profile_id  = profile_id["profile_id"],
        user_id     = view.user_id,
        type        = view.type
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    if new_add:
        return True
    else:
        return None
    
async def create_click_count(db: Session, click: ViewCountSchema):
    if click.type == "post":
        profile_id = await db.query(Posts.profile_id).filter(Posts.id == click.ads_id).first()
        db.close()
        
    if click.type == "ads":
        profile_id = await db.query(Ads.profile_id).filter(Ads.id == click.ads_id).first()
        db.close()
        
    if click.type == "banner":
        profile_id = await db.query(Images.profile_id).filter(Images.id == click.ads_id).first()
        db.close()
        
    if click.type == "popup":
        rofile_id = await db.query(PopUp.profile_id).filter(PopUp.id == click.ads_id).first()
        db.close()
        
    new_add = Ads2Profile_count(
        ads_id      = click.ads_id,
        profile_id  = profile_id["profile_id"],
        user_id     = click.user_id,
        type        = click.type
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    
    if new_add:
        return True
    else:
        return None
    
    
async def create_app_visitors(db: Session):
    new_add = AppVisitors()
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    
    if new_add:
        return True
    else:
        return None
    
    
async def create_like_dislike(db: Session, like: LikeDislikeSchema):
    if like.table_type == "post":
        if like.column_type == "like":
            db.query(Posts).filter(Posts.id == like.id)\
            .update({Posts.like : Posts.like + 1}, synchronize_session=False)
            db.commit()
            db.close()
            
            if like.type == True:
                get_dislike = db.query(Posts.dislike).filter(Posts.id == like.id).first()
                db.close()
                
                if get_dislike.dislike > 0:
                    db.query(Posts).filter(Posts.id == like.id)\
                    .update({Posts.dislike : Posts.dislike - 1}, synchronize_session=False)
                    db.commit()
                    db.close()    
        else:
            db.query(Posts).filter(Posts.id == like.id)\
            .update({Posts.dislike : Posts.dislike + 1}, synchronize_session=False)
            db.commit()
            db.close()
            if like.type == True:
                get_dislike = db.query(Posts.like).filter(Posts.id == like.id).first()
                db.close()
                if get_dislike.like > 0:
                    db.query(Posts).filter(Posts.id == like.id)\
                    .update({Posts.like : Posts.like - 1}, synchronize_session=False)
                    db.commit()   
                    db.close()
    else:
        if like.column_type == "like":
            db.query(Profiles).filter(Profiles.id == like.id)\
            .update({Profiles.like : Profiles.like + 1}, synchronize_session=False)
            db.commit()
            db.close()
            
            if like.type == True:
                get_dislike = db.query(Profiles.dislike).filter(Profiles.id == like.id).first()
                db.close()
                
                if get_dislike.dislike > 0:
                    db.query(Profiles).filter(Profiles.id == like.id)\
                    .update({Profiles.dislike : Profiles.dislike - 1}, synchronize_session=False)
                    db.commit()
                    db.close()
        else:
            db.query(Profiles).filter(Profiles.id == like.id)\
            .update({Profiles.dislike : Profiles.dislike + 1}, synchronize_session=False)
            db.commit()
            db.close()
            
            if like.type == True:
                get_dislike = db.query(Profiles.like).filter(Profiles.id == like.id).first()
                db.close()
                
                if get_dislike.like > 0:
                    db.query(Profiles).filter(Profiles.id == like.id)\
                    .update({Profiles.like : Profiles.like - 1}, synchronize_session=False)
                    db.commit()            
                    db.close()
                    
    return True


async def read_popup(db: Session):
    result = db.query(
        PopUp.id,
        PopUp.comment_of_admin,
        PopUp.image,
        PopUp.site_url,
        PopUp.titleTM,
        PopUp.titleRU,
        PopUp.descriptionTM,
        PopUp.descriptionRU,
        PopUp.profile_id
    )\
    .order_by(func.random())\
    .all()
    db.close()
    if result:
        return result
    else:
        return None
    
    
async def update_ticket_status(db: Session, id, ticket: TicketStatusUpdateSchema):
    new_update = db.query(TicketBron)\
    .filter(TicketBron.id == id)\
    .update({
        TicketBron.status : ticket.status
    }, synchronize_session=False)
    db.commit()
    db.close()
    
    if new_update:
        return True
    else:
        return None
    
    
async def read_user_info(db: Session, user_id):
    result = db.query(
        Users.id.label("user_id"),
        Users.fullname,
        Users.phone_number,
        CardUsers.date_of_birth,
        CardUsers.expired,
        CardUsers.gender,
        CardUsers.email,
        CardUsers.is_sms,
        CardUsers.status,
        CardUsers.card_id,
    )
    result = result.join(CardUsers, CardUsers.user_id == Users.id)
    result = result.filter(Users.id == user_id)
    result = result.filter(CardUsers.status == 1)
    result = result.filter(func.date(CardUsers.expired) >= datetime.now().date())
    result = result.distinct().all()
    db.close()
    
    if result:
        return result
    else:
        return None
    
    
    
async def read_admin_notif_token_by_cinema_id(db: Session, cinema_id):
    result = db.query(
        Admin.notif_token
    )\
    .filter(Admin.id == cinema_id)\
    .first()
    db.close()
    
    if result:
        return result
    else:
        return None
    
async def read_current_user(db: Session, user_id):
    result = db.query(
        Users.id,
        Users.fullname,
        Users.phone_number
    )
    result = result.filter(Users.id == user_id).first()
    if result:
        return result
    else:
        return None
    