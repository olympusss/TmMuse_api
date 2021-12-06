from sqlalchemy import Column, String, Integer, DateTime, Float, Boolean, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from db import Base

class Users(Base):
    __tablename__      = "users"
    id                 = Column(Integer, primary_key=True, index=True)
    fullname           = Column(String)
    phone_number       = Column(String)
    token              = Column(String)
    notif_token        = Column(Integer)
    created_at         = Column(DateTime, default=datetime.now())
    updated_at         = Column(DateTime, default=datetime.now())
    
    users_userinterests    = relationship("UserInterests")
    
    
class Interests(Base):
    __tablename__      = "interests"
    id                 = Column(Integer, primary_key=True, index=True)
    titleTM            = Column(String)
    titleRU            = Column(String)
    created_at         = Column(DateTime, default=datetime.now())
    updated_at         = Column(DateTime, default=datetime.now())
    
class InterestItems(Base):
    __tablename__      = "interest_items"
    id                 = Column(Integer, primary_key=True, index=True)
    titleTM            = Column(String)
    titleRU            = Column(String)
    interest_id        = Column(Integer)
    created_at         = Column(DateTime, default=datetime.now())
    updated_at         = Column(DateTime, default=datetime.now())
    
    interestitems_userinterests     = relationship("UserInterests")
    
    
class UserInterests(Base):
    __tablename__      = "user_interests"
    id                 = Column(Integer, primary_key=True, index=True)
    interest_item_id   = Column(Integer, ForeignKey("interest_items.id"))
    user_id            = Column(Integer, ForeignKey("users.id"))
    created_at         = Column(DateTime, default=datetime.now())
    updated_at         = Column(DateTime, default=datetime.now())
    
    
class Banners(Base):
    __tablename__      = "banners"
    id                 = Column(Integer, primary_key=True, index=True)
    image              = Column(String)
    link               = Column(String)
    order              = Column(Integer)
    profile_id         = Column(Integer, ForeignKey("profiles.id"))
    created_at         = Column(DateTime, default=datetime.now())
    updated_at         = Column(DateTime, default=datetime.now())
    
class Categories(Base):
    __tablename__      = "categories"
    id                 = Column(Integer, primary_key=True, index=True)
    name               = Column(String)
    created_at         = Column(DateTime, default=datetime.now())
    updated_at         = Column(DateTime, default=datetime.now())
    
    categories_profiles = relationship("Profiles")

class PhoneNumbers(Base):
    __tablename__      = "phone_numbers"
    id                 = Column(Integer, primary_key=True, index=True)
    phone_number       = Column(String)
    profile_id         = Column(Integer, ForeignKey("profiles.id"))
    created_at         = Column(DateTime, default=datetime.now())
    updated_at         = Column(DateTime, default=datetime.now())
    
class PromotionStatuses(Base):
    __tablename__      = "promotion_statuses"
    id                 = Column(Integer, primary_key=True, index=True)
    promotion_status   = Column(Float)
    profile_id         = Column(Integer, ForeignKey("profiles.id"))
    created_at         = Column(DateTime, default=datetime.now())
    updated_at         = Column(DateTime, default=datetime.now())
    
class Images(Base):
    __tablename__      = "images"
    id                 = Column(Integer, primary_key=True, index=True)
    small_image        = Column(String)
    large_image        = Column(String)
    isVR               = Column(Boolean)
    profile_id         = Column(Integer, ForeignKey("profiles.id"))
    created_at         = Column(DateTime, default=datetime.now())
    updated_at         = Column(DateTime, default=datetime.now())
    
class Profiles(Base):
    __tablename__      = "profiles"
    id                 = Column(Integer, primary_key=True, index=True)
    nameTM             = Column(String)
    nameRU             = Column(String)
    short_descTM       = Column(String)
    short_descRU       = Column(String)
    like               = Column(Integer)
    dislike            = Column(Integer)
    instagram          = Column(String)
    site               = Column(String)
    location           = Column(String)
    address            = Column(String)
    is_cash            = Column(Boolean)
    is_terminal        = Column(Boolean)
    work_hours         = Column(String) 
    delivery           = Column(Boolean)
    cousineTM          = Column(String)
    cousineRU          = Column(String)
    average_check      = Column(Float)
    is_active_card     = Column(Boolean)
    tm_muse_card       = Column(Float)
    is_certificate     = Column(Boolean)
    is_promo           = Column(Boolean)
    is_ads             = Column(Boolean)
    status             = Column(Integer)
    category_id        = Column(Integer, ForeignKey("categories.id"))
    view_count         = Column(Integer)
    promo_count        = Column(Integer)
    descriptionTM      = Column(String)
    descriptionRU      = Column(String)
    order_in_list      = Column(Integer)
    free_time          = Column(String)
    tenants_id         = Column(Integer)
    created_at         = Column(DateTime, default=datetime.now())
    updated_at         = Column(DateTime, default=datetime.now())
    
    profiles_images            = relationship("Images")
    profiles_promotionstatuses = relationship("PromotionStatuses")
    profiles_phonenumber       = relationship("PhoneNumbers")
    profiles_banners           = relationship("Banners")