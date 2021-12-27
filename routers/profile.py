from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db import get_db
from tokens import Returns, check_token, decode_token
from models import GetProfile, GetPromoCodes, AddCertificate
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
    results_ads = crud.read_ads_by_category_id(db=db, req=req)
    if not results_ads:
        return Returns.NULL
    results = {}
    results["profiles"] = results_profile
    results["ads"] = results_ads
    if results:
        return Returns.object(results)
    else:
        return Returns.NULL
    
    
@profile_router.get("/get-profile-tiny")
def get_profile_tiny(profile_id: int, db: Session = Depends(get_db)):
    result_profile        = crud.read_profile_by_profile_id(db=db, profile_id=profile_id)
    if not result_profile:
        return Returns.NULL
    results_promotion     = crud.read_promotion_by_profile_id(db=db, profile_id=profile_id)
    if not results_promotion:
        return Returns.NULL
    results_phone_numbers = crud.read_phone_numbers_by_profile_id(db=db, profile_id=profile_id)
    if not results_phone_numbers:
        return Returns.NULL
    results_images        = crud.read_images_by_profile_id(db=db, profile_id=profile_id)
    if not results_images:
        return Returns.NULL
    results_galleries     = crud.read_galleries_by_profile_id(db=db, profile_id=profile_id)
    if not results_galleries:
        return Returns.NULL
    results_posts         = crud.read_posts_by_profile_id(db=db, profile_id=profile_id)
    if not results_posts:
        return Returns.NULL
    results_certificates  = crud.read_certificates_by_profile_id(db=db, profile_id=profile_id)
    if not results_certificates:
        return Returns.NULL
    results_promo_codes   = crud.read_promo_codes_by_profile_id(db=db, profile_id=profile_id)
    if not results_promo_codes:
        return Returns.NULL
    results_tenants       = crud.read_tenants_by_profile_id(db=db, profile_id=profile_id)
    if not results_tenants:
        return Returns.NULL
    results_tags          = crud.read_tags_by_profile_id(db=db, profile_id=profile_id)
    if not results_tags:
        return Returns.NULL
    results_categories    = crud.read_category_by_profile_id(db=db, profile_id=profile_id)
    if not results_categories:
        return Returns.NULL
    results_ads           = crud.read_ads_by_join_category_id(db=db, profile_id=profile_id)
    if not results_ads:
        return Returns.NULL
    results = {}
    results["profile"]       = result_profile
    results["promotions"]    = results_promotion
    results["phone_numbers"] = results_phone_numbers
    results["images"]        = results_images
    results["galleries"]     = results_galleries
    results["posts"]         = results_posts
    results["certificates"]  = results_certificates
    results["promo_codes"]   = results_promo_codes
    results["tenants"]       = results_tenants
    results["tags"]          = results_tags
    results["categories"]    = results_categories
    results["ads"]           = results_ads
    if results:
        return Returns.object(results)
    else:
        Returns.NULL
        


@profile_router.post("/get-promo-codes")
def get_promo_codes(req: GetPromoCodes, header_param: Request, db: Session = Depends(get_db)):
    
    get_token = check_token(header_param=header_param)
    if not get_token:
        return Returns.TOKEN_NOT_FOUND
    
    payload = decode_token(token=get_token)
    if not payload:
        return Returns.TOKEN_NOT_DECODED
    
    fullname: str = payload.get("fullname")
    phone_number: str = payload.get("phone_number")
    user_id = crud.read_user_by_fullname_and_phone_number(db=db, fullname=fullname, phone_number=phone_number)
    if not user_id:
        return Returns.USER_NOT_FOUND
    
    # first condition
    profile_have_is_promo_eq_true = crud.read_profile_by_profile_id_filter_is_promo(db=db, profile_id=req.profile_id)
    if not profile_have_is_promo_eq_true:
        return Returns.NULL
    
    # second condition
    promo_code_have = crud.read_promo_codes_by_profile_id_user_id(db=db, profile_id=req.profile_id, user_id=user_id["id"])
    if promo_code_have:
        return Returns.object(promo_code_have)
    
    # third condition
    promo_code_count = crud.read_promo_code_count_by_profile_id(db=db, profile_id=req.profile_id)
    profile_promo_count = crud.read_profile_promo_count_by_profile_id(db=db, profile_id=req.profile_id)
    if promo_code_count >= profile_promo_count["promo_count"]:
        return Returns.LIMIT
    
    # fourth condition
    add_promo_count = crud.create_promo_code(db=db, userID=user_id["id"], profileID=req.profile_id)
    if add_promo_count:
        return Returns.INSERTED
    else:
        return Returns.NOT_INSERTED
    

@profile_router.post("/create-certificate")
def insert_certificate(req: AddCertificate, header_param: Request, db: Session = Depends(get_db)):
    get_token = check_token(header_param=header_param)
    if not get_token:
        return Returns.TOKEN_NOT_FOUND
    payload = decode_token(token=get_token)
    if not payload:
        return Returns.TOKEN_NOT_DECODED
    fullname: str = payload.get("fullname")
    phone_number: str = payload.get("phone_number")
    user_id = crud.read_user_by_fullname_and_phone_number(db=db, fullname=fullname, phone_number=phone_number)   
    
    insert_certificates = crud.create_certificates(db=db, req=req, userID=user_id["id"])
    if not insert_certificates:
        return Returns.NOT_INSERTED
    
    insert_inbox = crud.create_inbox_by_certificates(db=db, req=req, userID=user_id["id"])
    if not insert_inbox:
        return Returns.NOT_INSERTED
    
    get_inbox_id = crud.read_inbox_by_message(db=db, txt=insert_inbox)
    
    insert_send_user = crud.create_send_user(db=db, inboxID=get_inbox_id["id"], userID=user_id["id"])
    
    if insert_send_user:
        return Returns.INSERTED
    else:
        return Returns.NOT_INSERTED