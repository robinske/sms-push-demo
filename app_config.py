import os
from twilio.rest import Client
from authy.api import AuthyApiClient

client = Client(
    os.environ["TWILIO_ACCOUNT_SID"],
    os.environ["TWILIO_AUTH_TOKEN"]
)

authy_api = AuthyApiClient(os.environ["PUSH_DEMO_AUTHY_API_KEY"])
