class Returns:
    INSERTED     = {"error" : False, "body" : "INSERTED"}
    NOT_INSERTED = {"error" : True, "body" : "NOT INSERTED"}
    DELETED      = {"error" : False, "body" : "DELETED"}
    NOT_DELETED  = {"error" : True, "body" : "NOT DELETED"}
    
    def object(obj):
        return {"error" : False, "body" : obj}