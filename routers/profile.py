from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from tokens import Returns
from models import GetProfile
import crud

profile_router = APIRouter()

@profile_router.post("/get-profile")
def get_profile(req: GetProfile, db: Session = Depends(get_db)):
    results_profile = crud.read_profile(db=db, req=req)
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
    results_promotion     = crud.read_promotion_by_profile_id(db=db, profile_id=profile_id)
    results_phone_numbers = crud.read_phone_numbers_by_profile_id(db=db, profile_id=profile_id)
    results_images        = crud.read_images_by_profile_id(db=db, profile_id=profile_id)
    results_galleries     = crud.read_galleries_by_profile_id(db=db, profile_id=profile_id)
    results_posts         = crud.read_posts_by_profile_id(db=db, profile_id=profile_id)
    results_certificates  = crud.read_certificates_by_profile_id(db=db, profile_id=profile_id)
    results_promo_codes   = crud.read_promo_codes_by_profile_id(db=db, profile_id=profile_id)
    results_tenants       = crud.read_tenants_by_profile_id(db=db, profile_id=profile_id)
    results_tags          = crud.read_tags_by_profile_id(db=db, profile_id=profile_id)
    results_categories    = crud.read_category_by_profile_id(db=db, profile_id=profile_id)
    results_ads           = crud.read_ads_by_join_category_id(db=db, profile_id=profile_id)
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