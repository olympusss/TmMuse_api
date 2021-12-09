from fastapi import APIRouter, Depends, Request
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