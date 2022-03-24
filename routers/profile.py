from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from db import get_db
from tokens import Returns
from models import GetProfile, GetPromoCodes, AddCertificate
import crud

profile_router = APIRouter()

@profile_router.post("/get-profile")
async def get_profile(req: GetProfile, db: Session = Depends(get_db)):
    results_profile = await crud.read_profile(db=db, req=req)
    if not results_profile:
        return Returns.NULL 
    results = {}
    results["profiles"] = results_profile 
    if req.page == 1: 
        results_ads = await crud.read_ads_random(db=db)
        results["ads"] = results_ads
    if len(req.category) > 0:
        results_tags = []
        for i in req.category:
            get_tags = await crud.read_tags_by_category_id(db=db, category_id=i)
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
    result_profile = await crud.read_profile_by_profile_id(db=db, profile_id=profile_id)
    if result_profile:
        results["profile"] = result_profile
    results_phone_numbers = await crud.read_phone_numbers_by_profile_id(db=db, profile_id=profile_id)
    if results_phone_numbers:
        results["phone_numbers"] = results_phone_numbers
    results_images = await crud.read_images_by_profile_id(db=db, profile_id=profile_id)
    if results_images:
        results["images"] = results_images
    results_galleries = await crud.read_galleries_by_profile_id(db=db, profile_id=profile_id)
    if results_galleries:
        results["galleries"] = results_galleries
    results_posts = await crud.read_posts_by_profile_id(db=db, profile_id=profile_id)
    if results_posts:
        results["posts"] = results_posts
    results_certificates = await crud.read_certificates_by_profile_id(db=db, profile_id=profile_id)
    if results_certificates:
        results["certificates"] = results_certificates
    results_promo_codes = await crud.read_promo_codes_by_profile_id(db=db, profile_id=profile_id)
    if results_promo_codes:
        results["promo_codes"] = results_promo_codes
    results_tags = await crud.read_tags_by_profile_id(db=db, profile_id=profile_id)
    if results_tags:
        results["tags"] = results_tags
    results_categories = await crud.read_category_by_profile_id(db=db, profile_id=profile_id)
    if results_categories:
        results["categories"] = results_categories
    results_ads = await crud.read_ads_by_join_category_id(db=db, profile_id=profile_id)
    if results_ads:
        results["ads"] = results_ads
    if results:
        return Returns.object(results)
    else:
        return Returns.NULL
        


@profile_router.post("/get-promo-codes", dependencies=[Depends(HTTPBearer())])
async def get_promo_codes(req: GetPromoCodes, header_param: Request, db: Session = Depends(get_db)):

    user_id = await crud.read_user_id_from_token(db=db, header_param=header_param)
    
    # first condition
    profile_have_is_promo_eq_true = await crud.read_profile_by_profile_id_filter_is_promo(db=db, profile_id=req.profile_id)
    if not profile_have_is_promo_eq_true:
        return Returns.PROMO_CAN_NOT_CREATE
    
    # second condition
    promo_code_have = await crud.read_promo_codes_by_profile_id_user_id(db=db, profile_id=req.profile_id, user_id=user_id)
    if promo_code_have:
        return Returns.object(promo_code_have[0]["promo_code"])
    
    # third condition
    promo_code_count = await crud.read_promo_code_count_by_profile_id(db=db, profile_id=req.profile_id)
    profile_promo_count = await crud.read_profile_promo_count_by_profile_id(db=db, profile_id=req.profile_id)
    print(promo_code_count, profile_promo_count)
    if promo_code_count >= profile_promo_count["promo_count"]:
        return Returns.LIMIT
    
    # fourth condition
    add_promo_count = await crud.create_promo_code(db=db, userID=user_id, profileID=req.profile_id)
    if add_promo_count:
        return Returns.object(add_promo_count)
    else:
        return Returns.NOT_INSERTED
    

@profile_router.post("/create-certificate", dependencies=[Depends(HTTPBearer())])
async def insert_certificate(req: AddCertificate, header_param: Request, db: Session = Depends(get_db)):
    user_id = await crud.read_user_id_from_token(db=db, header_param=header_param)   
    
    insert_certificates = await crud.create_certificates(db=db, req=req, userID=user_id)
    if not insert_certificates:
        return Returns.NOT_INSERTED
    
    insert_inbox = await crud.create_inbox_by_certificates(db=db, req=req, userID=user_id)
    if not insert_inbox:
        return Returns.NOT_INSERTED
    
    get_inbox_id = await crud.read_inbox_by_message(db=db, txt=insert_inbox)
    
    insert_send_user = await crud.create_send_user(db=db, inboxID=get_inbox_id["id"], userID=user_id)
    
    if insert_send_user:
        return Returns.INSERTED
    else:
        return Returns.NOT_INSERTED