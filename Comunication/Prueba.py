import os
from twilio.rest import Client
import sys
sys.path.append("..")  # Agrega el directorio anterior al PATH
from TwilioConfig import PHONE_NUMBER_FROM, PHONE_NUMBER_TO, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, API_KEY_WAPI, COORDINATE
import logging
logging.basicConfig(level=logging.DEBUG)

account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN
phone_number_from = PHONE_NUMBER_FROM
phone_number_to = PHONE_NUMBER_TO
client = Client(account_sid, auth_token)


if __name__ == "__main__":

    message = client.messages.create(
            body = "Primera prueba",
            from_ = phone_number_from,
            to =  phone_number_to
        )
    logging.info(message.sid)
    
