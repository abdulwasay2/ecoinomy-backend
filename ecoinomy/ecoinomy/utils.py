# import TextMagic
# from TextMagic.rest import ApiException
from traceback import print_exc
from twilio.rest import Client
from django.conf import settings


# def send_text_message_text_magic(message, recipient_phone_nums):
#     try:
#         configuration = TextMagic.Configuration()
#         configuration.username = settings.TEXTMAGIC_USERNAME
#         configuration.password = settings.TEXTMAGIC_PASSWORD
#         api_instance = TextMagic.TextMagicApi(TextMagic.ApiClient(configuration))

#         send_message_input_object = TextMagic.SendMessageInputObject()
#         send_message_input_object.text = message
#         send_message_input_object.phones = ",".join(recipient_phone_nums)
        
#         response = api_instance.send_message(send_message_input_object)
#         return response
#     except ApiException as e:
#         print("Exception when calling TextMagicApi->send_message: %s\n" % e)


def send_text_message_twilio(message, recipient_phone_num):

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    try:
        twilio_message = client.messages.create(
            to=recipient_phone_num,
            from_=settings.TWILIO_PHONE_NUMBER,
            body=message)

        print("Twilio message queued with id:", twilio_message.sid)
        print(twilio_message.body)
    except:
        print("Twilio message sending failed.")
        print_exc()