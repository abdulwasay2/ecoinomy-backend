import TextMagic
from TextMagic.rest import ApiException
from django.conf import settings


def send_text_message_text_magic(message, recipient_phone_nums):
    try:
        configuration = TextMagic.Configuration()
        configuration.username = settings.TEXTMAGIC_USERNAME
        configuration.password = settings.TEXTMAGIC_PASSWORD
        api_instance = TextMagic.TextMagicApi(TextMagic.ApiClient(configuration))

        send_message_input_object = TextMagic.SendMessageInputObject()
        send_message_input_object.text = message
        send_message_input_object.phones = ",".join(recipient_phone_nums)
        
        response = api_instance.send_message(send_message_input_object)
        return response
    except ApiException as e:
        print("Exception when calling TextMagicApi->send_message: %s\n" % e)