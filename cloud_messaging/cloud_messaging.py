import firebase_admin
from firebase_admin import messaging
from firebase_admin import credentials

cred = credentials.Certificate("/home/tmmuse_server/TmMuse_api/cloud_messaging/cloud_messaging_credential.json")
# cred = credentials.Certificate("D:\\Project\\TmMuse_api\\cloud_messaging\\cloud_messaging_credential.json")
default_app = firebase_admin.initialize_app(cred)

# * Send to token
async def send_to_token(token: str, data, date: str, time: str, count_ticket: int):
    title = "Täze petek sargyt edildi / Заказан новый билеты"
    bodyTM = "Siziň {} senedäki sagat {}-da boljak filmiňize {} sany täze petek sargyt edildi\n\n".format(date, time, count_ticket)
    bodyRU = "На ваш фильм {} в {} заказано {} новых билета.".format(date, time, count_ticket)
    body = bodyTM + bodyRU
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        data=data,
        token=token
    )
    
    response = messaging.send(message=message)
    print("Successfully sent message to token: ", response)