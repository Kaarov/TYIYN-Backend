import firebase_admin
from django.conf import settings
from firebase_admin import credentials, messaging

from users.models import User

# Initializing the Firebase Admin SDK (do this only once)
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred)
        print("Firebase Admin SDK initialized successfully.")
    except FileNotFoundError:
        print(f"Error: The Firebase credential file was not found on the path.: {settings.FIREBASE_CREDENTIALS_PATH}")
    except Exception as e:
        print(f"Firebase Admin SDK Initialization error: {e}")


def send_push_notification(user, title, body):
    """
    Sends a push notification to the user via Firebase.
    You will need to implement the logic for obtaining the user's device token.
    """
    print("Отправка уведомления пользователю")
    try:
        # device_token = user.fcm_token
        device_token = "e09AV9mcSrS7HEe2JQ61vp:APA91bHSRyQOZBDmeaV7ah12gwT22ba0nI8GsDnvkjik_jZhVeWDNiVbHQ0e7wptenGc1coHFp3eue_iUpFsYdeMfPHcXkQgjv5asodYBh0qNslReEAKjV8"
        print("Отправка уведомления пользователю")

        if device_token:
            print(f"Отправка уведомления пользователю {user.username}: '{title}' - '{body}'")
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                token=device_token,
            )
            print("!!!!message, ", message)
            response = messaging.send(message)
            print("Successfully sent message:", response)
    except Exception as e:
        print(f"Error sending notification: {e}")
