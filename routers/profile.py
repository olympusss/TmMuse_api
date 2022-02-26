from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from db import get_db
from tokens import Returns, check_token, decode_token
from models import GetProfile, GetPromoCodes, AddCertificate, Categories
import crud

profile_router = APIRouter()

@profile_router.post("/get-profile")
def get_profile(req: GetProfile, db: Session = Depends(get_db)):
    results_profile = crud.read_profile(db=db, req=req)
    if not results_profile:
        return Returns.NULL
    newList = []
    for elem in results_profile:
        elem = dict(elem)
        promotion = crud.read_promotion_by_profile_id(db=db, profile_id=elem["id"])
        if promotion:
            elem["is_promotion"] = True
            elem["promotion_status"] = promotion["promotion_status"]
        else:
            elem["is_promotion"] = False
            elem["promotion_status"] = 0
        newList.append(elem)
    results_profile = newList  
    results = {}
    results["profiles"] = results_profile 
    if req.page == 1: 
        results_ads = crud.read_ads_random(db=db)
        results["ads"] = results_ads
    if len(req.category) > 0:
        results_tags = []
        for i in req.category:
            get_tags = crud.read_tags_by_category_id(db=db, category_id=i)
            for tag in get_tags:
                results_tags.append(tag)
        results["tags"] = results_tags
    if results:
        return Returns.object(results)
    else:
        return Returns.NULL
    
    
@profile_router.get("/get-profile-tiny")
async def get_profile_tiny(profile_id: int, db: Session = Depends(get_db)):
    results = {}
    await crud.create_profile_view(db=db, profile_id=profile_id)
    result_profile = crud.read_profile_by_profile_id(db=db, profile_id=profile_id)
    if result_profile:
        results["profile"] = result_profile
    results_promotion = crud.read_promotion_by_profile_id(db=db, profile_id=profile_id)
    if results_promotion:
        results["promotions"] = results_promotion
    results_phone_numbers = crud.read_phone_numbers_by_profile_id(db=db, profile_id=profile_id)
    if results_phone_numbers:
        results["phone_numbers"] = results_phone_numbers
    results_images = crud.read_images_by_profile_id(db=db, profile_id=profile_id)
    if results_images:
        results["images"]        = results_images
    results_galleries = crud.read_galleries_by_profile_id(db=db, profile_id=profile_id)
    if results_galleries:
        results["galleries"]     = results_galleries
    results_posts = crud.read_posts_by_profile_id(db=db, profile_id=profile_id)
    if results_posts:
        results["posts"]         = results_posts
    results_certificates = crud.read_certificates_by_profile_id(db=db, profile_id=profile_id)
    if results_certificates:
        results["certificates"]  = results_certificates
    results_promo_codes = crud.read_promo_codes_by_profile_id(db=db, profile_id=profile_id)
    if results_promo_codes:
        results["promo_codes"]   = results_promo_codes
    results_tags = crud.read_tags_by_profile_id(db=db, profile_id=profile_id)
    if results_tags:
        results["tags"]          = results_tags
    results_categories = crud.read_category_by_profile_id(db=db, profile_id=profile_id)
    if results_categories:
        results["categories"]    = results_categories
    results_ads = crud.read_ads_by_join_category_id(db=db, profile_id=profile_id)
    if results_ads:
        results["ads"]           = results_ads
    if results:
        return Returns.object(results)
    else:
        return Returns.NULL
        


@profile_router.post("/get-promo-codes", dependencies=[Depends(HTTPBearer())])
def get_promo_codes(req: GetPromoCodes, header_param: Request, db: Session = Depends(get_db)):

    user_id = crud.read_user_id_from_token(db=db, header_param=header_param)
    
    # first condition
    profile_have_is_promo_eq_true = crud.read_profile_by_profile_id_filter_is_promo(db=db, profile_id=req.profile_id)
    if not profile_have_is_promo_eq_true:
        return Returns.PROMO_CAN_NOT_CREATE
    
    # second condition
    promo_code_have = crud.read_promo_codes_by_profile_id_user_id(db=db, profile_id=req.profile_id, user_id=user_id)
    if promo_code_have:
        return Returns.object(promo_code_have[0]["promo_code"])
    
    # third condition
    promo_code_count = crud.read_promo_code_count_by_profile_id(db=db, profile_id=req.profile_id)
    profile_promo_count = crud.read_profile_promo_count_by_profile_id(db=db, profile_id=req.profile_id)
    if promo_code_count >= profile_promo_count["promo_count"]:
        return Returns.LIMIT
    
    # fourth condition
    add_promo_count = crud.create_promo_code(db=db, userID=user_id, profileID=req.profile_id)
    if add_promo_count:
        return Returns.object(add_promo_count)
    else:
        return Returns.NOT_INSERTED
    

@profile_router.post("/create-certificate", dependencies=[Depends(HTTPBearer())])
def insert_certificate(req: AddCertificate, header_param: Request, db: Session = Depends(get_db)):
    user_id = crud.read_user_id_from_token(db=db, header_param=header_param)   
    
    insert_certificates = crud.create_certificates(db=db, req=req, userID=user_id)
    if not insert_certificates:
        return Returns.NOT_INSERTED
    
    insert_inbox = crud.create_inbox_by_certificates(db=db, req=req, userID=user_id)
    if not insert_inbox:
        return Returns.NOT_INSERTED
    
    get_inbox_id = crud.read_inbox_by_message(db=db, txt=insert_inbox)
    
    insert_send_user = crud.create_send_user(db=db, inboxID=get_inbox_id["id"], userID=user_id)
    
    if insert_send_user:
        return Returns.INSERTED
    else:
        return Returns.NOT_INSERTED