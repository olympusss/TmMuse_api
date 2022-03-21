class Returns:
    INSERTED                       = {"error" : False, "body" : "INSERTED"}
    NOT_INSERTED                   = {"error" : True,  "body" : "NOT INSERTED"}
    DELETED                        = {"error" : False, "body" : "DELETED"}
    NOT_DELETED                    = {"error" : True,  "body" : "NOT DELETED"}
    UPDATED                        = {"error" : False, "body" : "UPDATED"}
    NOT_UPDATED                    = {"error" : True,  "body" : "NOT UPDATED"}
    NULL                           = {"error" : True,  "body" : None}
    TOKEN_NOT_FOUND                = {"error" : True,  "body" : "TOKEN_NOT_FOUND"}
    TOKEN_NOT_DECODED              = {"error" : True,  "body" : "TOKEN_NOT_DECODED"}
    USER_NOT_FOUND                 = {"error" : True,  "body" : "USER_NOT_FOUND"}
    LIMIT                          = {"error" : True,  "body" : "LIMIT"}
    WRONG_CODE                     = {"error" : True,  "body" : "WRONG_CODE"}
    TIMEOUT                        = {"error" : True,  "body" : "TIMEOUT"}
    PROMO_CAN_NOT_CREATE           = {"error" : True,  "body" : "PROMO_CAN_NOT_CREATE"}
    TICKET_NOT_FOUND               = {"error" : True,  "body" : "TICKET_NOT_FOUND"}
    CURRENT_ADMIN_NOT_FOUND        = {"error" : True,  "body" : "CURRENT_ADMIN_NOT_FOUND"}
    NOT_SENDED_TO_PUSH             = {"error" : True,  "body" : "NOT_SENDED_TO_PUSH"}
    
    def object(obj):
        return {"error" : False, "body" : obj}
    
    def id(obj):
        return {"error" : False, "body" : {"INSERTED_ID" : obj}}