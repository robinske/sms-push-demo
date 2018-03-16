import os
from twilio.rest import Client

client = Client(
    os.environ["TWILIO_ACCOUNT_SID"],
    os.environ["TWILIO_AUTH_TOKEN"]
)

MY_NUMBER = os.environ["TWILIO_AUTH_TOKEN"]
