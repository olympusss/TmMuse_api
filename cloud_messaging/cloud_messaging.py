import firebase_admin
from firebase_admin import messaging
from firebase_admin import credentials

cred = credentials.Certificate("/home/tmmuse_server/TmMuse_mobile/cloud_messaging/cloud_messaging_credential.json")
# cred = credentials.Certificate("D:\\Project\\TmMuse_api\\cloud_messaging\\cloud_messaging_credential.json")
default_app = firebase_admin.initialize_app(cred)


# * Send to token
async def send_to_token(token: str, ticket_id: str, date: str, time: str, count_ticket: int):
    title = "Täze petek sargyt edildi / Заказан новый билет"
    bodyTM = f"Siziň {date} senedäki sagat {time}-da boljak filmiňize {count_ticket} sany täze petek sargyt edildi\n\n"
    bodyRU = f"На ваш фильм {date} в {time} заказано {count_ticket} новых билета."
    body = bodyTM + bodyRU
    send = {"ticket_id" : ticket_id}
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        data=send,
        token=token
    )
    
    response = messaging.send(message=message)
    print("Successfully sent message to token: ", response)
    
    
async def send_to_topic(topic, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        topic=topic
    )
    
    response = messaging.send(message=message)
    print("Successfully sent message to topic: ", response)