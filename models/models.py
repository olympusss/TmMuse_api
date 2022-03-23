from sqlalchemy import Column, String, Integer, DateTime, Float, Boolean, ForeignKey, Date, Time
from datetime import datetime
from sqlalchemy.orm import relationship
from db import Base

class Users(Base):
    __tablename__      = "users"
    id                 = Column(Integer, primary_key=True, index=True)
    fullname           = Column(String)
    phone_number       = Column(String)
    token              = Column(String)
    notif_token        = Column(String)
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    users_userinterests = relationship("UserInterests", back_populates="userinterests_users")
    users_certificates  = relationship("Certificates" , back_populates="certificates_users")
    users_promocodes    = relationship("PromoCodes"   , back_populates="promocodes_users")
    users_senduser      = relationship("SendUser"     , back_populates="senduser_users")
    users_cardusers     = relationship("CardUsers"    , back_populates="cardusers_users")
    users_ticketbron    = relationship("TicketBron"   , back_populates="ticketbron_users")
    
    
    
    
class Interests(Base):
    __tablename__      = "interests"
    id                 = Column(Integer, primary_key=True, index=True)
    titleTM            = Column(String)
    titleRU            = Column(String)
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    interests_interestitems = relationship("InterestItems", back_populates="interestitems_interests")
    
    
class InterestItems(Base):
    __tablename__      = "interest_items"
    id                 = Column(Integer, primary_key=True, index=True)
    titleTM            = Column(String)
    titleRU            = Column(String)
    interest_id        = Column(Integer, ForeignKey("interests.id"))
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    interestitems_userinterests = relationship("UserInterests", back_populates="userinterests_interestitems")
    interestitems_interests = relationship("Interests", back_populates="interests_interestitems")
    
    
class UserInterests(Base):
    __tablename__      = "user_interests"
    id                 = Column(Integer, primary_key=True, index=True)
    interest_item_id   = Column(Integer, ForeignKey("interest_items.id"))
    user_id            = Column(Integer, ForeignKey("users.id"))
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    userinterests_users         = relationship("Users", back_populates="users_userinterests")
    userinterests_interestitems = relationship("InterestItems", back_populates="interestitems_userinterests")
    
     
class Banners(Base):
    __tablename__      = "banners"
    id                 = Column(Integer, primary_key=True, index=True)
    image              = Column(String)
    link               = Column(String)
    order              = Column(Integer)
    comment_of_admin   = Column(String)
    profile_id         = Column(Integer, ForeignKey("profiles.id"))
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    banners_profiles   = relationship("Profiles" , back_populates="profiles_banners")
    
    
class Categories(Base):
    __tablename__      = "categories"
    id                 = Column(Integer, primary_key=True, index=True)
    name               = Column(String)
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    categories_profiles        = relationship("Profiles", back_populates="profiles_categories")
    categories_joincategoryads = relationship("JoinCategoryAds", back_populates="joincategoryads_categories")
    categories_tags            = relationship("Tags", back_populates="tags_categories")
    
    
class PhoneNumbers(Base):
    __tablename__      = "phone_numbers"
    id                 = Column(Integer, primary_key=True, index=True)
    phone_number       = Column(String)
    profile_id         = Column(Integer, ForeignKey("profiles.id"))
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    phonenumbers_profiles = relationship("Profiles", back_populates="profiles_phonenumbers")
    
    
class Images(Base):
    __tablename__      = "images"
    id                 = Column(Integer, primary_key=True, index=True)
    small_image        = Column(String)
    large_image        = Column(String)
    isVR               = Column(Boolean, default=False)
    profile_id         = Column(Integer, ForeignKey("profiles.id"))
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    images_profiles    = relationship("Profiles", back_populates="profiles_images")
    
    
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
    is_cash            = Column(Boolean, default=False)
    is_terminal        = Column(Boolean, default=False)
    work_hours         = Column(String) 
    delivery           = Column(Boolean, default=False)
    cousineTM          = Column(String)
    cousineRU          = Column(String)
    average_check      = Column(Float)
    is_active_card     = Column(Boolean, default=False)
    tm_muse_card       = Column(Float)
    is_certificate     = Column(Boolean, default=False)
    is_VIP             = Column(Integer)
    is_promo           = Column(Boolean, default=False)
    WiFi               = Column(Boolean)
    status             = Column(Integer)
    category_id        = Column(Integer, ForeignKey("categories.id"))
    cinema_id          = Column(Integer)
    view_count         = Column(Integer)
    promo_count        = Column(Integer)
    descriptionTM      = Column(String)
    descriptionRU      = Column(String)
    order_in_list      = Column(Integer)
    free_time          = Column(String)
    required_promotion = Column(Boolean)
    own_promotion      = Column(Float)
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    
    profiles_images            = relationship("Images"              , back_populates="images_profiles")
    profiles_phonenumbers      = relationship("PhoneNumbers"        , back_populates="phonenumbers_profiles")
    profiles_banners           = relationship("Banners"             , back_populates="banners_profiles")
    profiles_categories        = relationship("Categories"          , back_populates="categories_profiles")
    profiles_ads               = relationship("Ads"                 , back_populates="ads_profiles")
    profiles_galleries         = relationship("Galleries"           , back_populates="galleries_profiles")
    profiles_posts             = relationship("Posts"               , back_populates="posts_profiles")
    profiles_certificates      = relationship("Certificates"        , back_populates="certificates_profiles")
    profiles_promocodes        = relationship("PromoCodes"          , back_populates="promocodes_profiles")
    profiles_popup             = relationship("PopUp"               , back_populates="popup_profiles")
    profiles_ticketbron        = relationship("TicketBron"          , back_populates="ticketbron_profiles")
    profiles_tags              = relationship("Tags"                , back_populates="tags_profiles")
    



class Ads(Base):
    __tablename__      = "ads"
    id                 = Column(Integer, primary_key=True, index=True)
    nameTM             = Column(String)
    nameRU             = Column(String)
    comment_of_admin   = Column(String)
    image              = Column(String)
    is_main            = Column(Boolean)
    site_url           = Column(String)
    profile_id         = Column(Integer, ForeignKey("profiles.id"))
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    ads_profiles        = relationship("Profiles", back_populates="profiles_ads")
    ads_joincategoryads = relationship("JoinCategoryAds", back_populates="joincategoryads_ads")
    
    
class JoinCategoryAds(Base):
    __tablename__      = "join_category_ads"
    id                 = Column(Integer, primary_key=True, index=True)
    ads_id             = Column(Integer, ForeignKey("ads.id"))
    category_id        = Column(Integer, ForeignKey("categories.id"))
    joincategoryads_ads        = relationship("Ads", back_populates="ads_joincategoryads")
    joincategoryads_categories = relationship("Categories", back_populates="categories_joincategoryads")
    
    
class Tags(Base):
    __tablename__      = "tags"
    id                 = Column(Integer, primary_key=True, index=True)
    tagTM              = Column(String)
    tagRU              = Column(String)
    category_id        = Column(Integer, ForeignKey("categories.id"))
    profile_id         = Column(Integer, ForeignKey("profiles.id"))
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    tags_profiles      = relationship("Profiles" , back_populates="profiles_tags")
    tags_categories    = relationship("Categories", back_populates="categories_tags")
    
    
    
class Galleries(Base):
    __tablename__      = "galleries"
    id                 = Column(Integer, primary_key=True, index=True)
    medium_image       = Column(String)
    large_image        = Column(String)
    profile_id         = Column(Integer, ForeignKey("profiles.id"))
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    galleries_profiles = relationship("Profiles", back_populates="profiles_galleries")
    
    
class Posts(Base):
    __tablename__      = "posts"
    id                 = Column(Integer, primary_key=True, index=True)
    titleTM            = Column(String)
    titleRU            = Column(String)
    descriptionTM      = Column(String)
    descriptionRU      = Column(String)
    comment_of_admin   = Column(String)
    status             = Column(Boolean)
    image              = Column(String)
    promotion          = Column(Float)
    view_count         = Column(Integer, default = 0)
    like               = Column(Integer)
    dislike            = Column(Integer)
    profile_id         = Column(Integer, ForeignKey("profiles.id"))
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    posts_profiles     = relationship("Profiles", back_populates="profiles_posts")
    
    
class Certificates(Base):
    __tablename__      = "certificates"
    id                 = Column(Integer, primary_key=True, index=True)
    amount             = Column(Float)
    status             = Column(Integer)
    profile_id         = Column(Integer, ForeignKey("profiles.id"))
    user_id            = Column(Integer, ForeignKey("users.id"))
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    certificates_profiles = relationship("Profiles", back_populates="profiles_certificates")
    certificates_users    = relationship("Users"   , back_populates="users_certificates")
    
    
class PromoCodes(Base):
    __tablename__      = "promo_codes"
    id                 = Column(Integer, primary_key=True, index=True)
    promo_code         = Column(String)
    status             = Column(Integer)
    profile_id         = Column(Integer, ForeignKey("profiles.id"))
    user_id            = Column(Integer, ForeignKey("users.id"))
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    promocodes_profiles = relationship("Profiles", back_populates="profiles_promocodes")
    promocodes_users    = relationship("Users"   , back_populates="users_promocodes")
    
    
class Inbox(Base):
    __tablename__      = "inbox"
    id                 = Column(Integer, primary_key=True, index=True)
    title              = Column(String)
    message            = Column(String)
    is_all             = Column(Boolean)
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    inbox_senduser     = relationship("SendUser", back_populates="senduser_inbox")
    inbox_answers      = relationship("Answers" , back_populates="answers_inbox")
    
     
class SendUser(Base):
    __tablename__      = "send_user"
    id                 = Column(Integer, primary_key=True, index=True)
    is_read            = Column(Boolean, default=False)
    user_id            = Column(Integer, ForeignKey("users.id"))
    inbox_id           = Column(Integer, ForeignKey("inbox.id"))
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    senduser_inbox     = relationship("Inbox", back_populates="inbox_senduser")
    senduser_users     = relationship("Users", back_populates="users_senduser")
    
    
class AnsweredMessages(Base):
    __tablename__      = "answered_messages"
    id                 = Column(Integer, primary_key=True, index=True)
    title              = Column(String)
    message            = Column(String)
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    answeredmessages_answers = relationship("Answers", back_populates="answers_answeredmessages")
    
    
class Answers(Base):
    __tablename__      = "answers"
    id                 = Column(Integer, primary_key=True, index=True)
    answered_msg_id    = Column(Integer, ForeignKey("answered_messages.id"))
    inbox_id           = Column(Integer, ForeignKey("inbox.id"))
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    answers_inbox            = relationship("Inbox", back_populates="inbox_answers")
    answers_answeredmessages = relationship("AnsweredMessages", back_populates="answeredmessages_answers")
    
    
class CardUsers(Base):
    __tablename__      = "card_users"
    id                 = Column(Integer, primary_key=True, index=True)
    date_of_birth      = Column(Date)
    expired            = Column(Date)
    gender             = Column(Integer)
    email              = Column(String)
    is_sms             = Column(Boolean)
    status             = Column(Integer)
    card_id            = Column(String)
    user_id            = Column(Integer, ForeignKey("users.id"))
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    cardusers_users    = relationship("Users", back_populates="users_cardusers")
    
    
   
    
class Constants(Base):
    __tablename__      = "constants"
    id                 = Column(Integer, primary_key=True, index=True)
    titleTM            = Column(String)
    titleRU            = Column(String)
    contentTM          = Column(String)
    contentRU          = Column(String)
    contentTM_dark     = Column(String)
    contentRU_dark     = Column(String)
    type               = Column(String)
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    
    
class SearchHistory(Base):
    __tablename__      = "search_history"
    id                 = Column(Integer, primary_key=True, index=True)
    text               = Column(String)
    count              = Column(Integer)
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    

class Admin(Base):
    __tablename__      = "admin"
    id                 = Column(Integer, primary_key=True, index=True)
    username           = Column(String)
    password           = Column(String)
    token              = Column(String)
    notif_token        = Column(String)
    type               = Column(Integer, ForeignKey('admin_type.id'))
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    admin_admintype    = relationship('AdminType', back_populates='admintype_admin')
    admin_ticketbron   = relationship("TicketBron"  , back_populates="ticketbron_admin")
    
    
    
class AdminType(Base):
    __tablename__      = "admin_type"
    id                 = Column(Integer, primary_key=True, index=True)
    type               = Column(String)
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    admintype_admin    = relationship('Admin', back_populates='admin_admintype')
    
    
class PopUp(Base):
    __tablename__      = "pop_up"
    id                 = Column(Integer, primary_key=True, index=True)
    comment_of_admin   = Column(String)
    image              = Column(String)
    site_url           = Column(String)
    titleTM            = Column(String)
    titleRU            = Column(String)
    descriptionTM      = Column(String)
    descriptionRU      = Column(String)
    profile_id         = Column(Integer, ForeignKey("profiles.id"))
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    popup_profiles     = relationship("Profiles", back_populates="profiles_popup")
    
    
class NumberSocket(Base):
    __tablename__      = "number_socket"
    id                 = Column(Integer, primary_key=True, index=True)
    phone_number       = Column(String)
    code               = Column(String)
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    
    
class ProfileView(Base):
    __tablename__      = "profile_view"
    id                 = Column(Integer, primary_key=True, index=True)
    user_id            = Column(Integer)
    profile_id         = Column(Integer)
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    
    
class Ads2Profile_count(Base):
    __tablename__      = "ads2profile_count"
    id                 = Column(Integer, primary_key=True, index=True)
    user_id            = Column(Integer)
    profile_id         = Column(Integer)
    ads_id             = Column(Integer)
    type               = Column(String)
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    
class AdsView(Base):
    __tablename__      = "ads_view"
    id                 = Column(Integer, primary_key=True, index=True)
    user_id            = Column(Integer)
    profile_id         = Column(Integer)
    ads_id             = Column(Integer)
    type               = Column(String)
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    
    
class AppVisitors(Base):
    __tablename__      = "app_visitors"
    id                 = Column(Integer, primary_key=True, index=True)
    user_id            = Column(Integer)
    created_at         = Column(DateTime(timezone=False), default=datetime.now)
    updated_at         = Column(DateTime(timezone=False), default=datetime.now)
    
class TicketBron(Base):
    __tablename__       = "ticket_bron"
    id                  = Column(Integer, primary_key=True, index=True)
    cinema_id           = Column(Integer, ForeignKey("admin.id"))
    profile_id          = Column(Integer, ForeignKey("profiles.id"))
    user_id             = Column(Integer, ForeignKey("users.id"))
    movie_date          = Column(Date)
    movie_time          = Column(Time)
    ticket_count        = Column(Integer)
    ticket_price        = Column(Float)
    ticket_discount     = Column(Float)
    status              = Column(Integer)
    created_at          = Column(DateTime(timezone=False), default=datetime.now)
    updated_at          = Column(DateTime(timezone=False), default=datetime.now)
    ticketbron_admin    = relationship("Admin"      , back_populates="admin_ticketbron")
    ticketbron_profiles = relationship("Profiles"   , back_populates="profiles_ticketbron")
    ticketbron_users    = relationship("Users"      , back_populates="users_ticketbron")