import os
import random
import phonenumbers as pn

from flask import Flask, Response, request

from authy.api import AuthyApiClient
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

authy_api = AuthyApiClient(os.environ["PUSH_DEMO_AUTHY_API_KEY"])
TWILIO_NUMBER = os.environ["PUSH_DEMO_FROM"]
client = Client()


app = Flask(__name__)


def _push(phone, text):
    """
    Returns the uuid of the push notification, otherwise sends
    """
    country_code = phone.country_code
    number = phone.national_number

    user = authy_api.users.create(
        'stub@myemail.com',
        number,
        country_code)

    status = authy_api.users.status(user.id)
    if status.ok():
        devices = status.content['status'].get('devices')

    # No Authy App installed, send user link to download
    if not devices:
        message = "Download the Authy App to receive your notification: https://authy.com/download/"
        return message

    logo = {
        'res': 'default',
        'url': 'https://github.com/robinske/sms-push-demo/blob/master/wave.png?raw=true'
    }

    phone_number = str(country_code) + str(number)
    details = {
        'Account Number': str(user.id),
        'Phone Number': phone_number
    }

    usernames = ['Opalescent Tree Shark', 'Perfect Sunflower', 'Rainbow Infused Space Unicorn', 'Beautiful Rule-breaking Moth']

    details['Username'] = random.choice(usernames)
    message = "You said: {}".format(text)

    response = authy_api.one_touch.send_request(
        user.id,
        message,
        seconds_to_expire=1200,
        details=details,
        logos=[logo])

    if response.ok():
        message = "Check your Authy app for a push notification!"
        # Add note about downloading if first time texting this number
        prev_messages = client.messages.list(from_=TWILIO_NUMBER, to=phone_number)
        if not prev_messages:
            message = message + " If you need to download the app, visit https://authy.com/download/"
        return message
    else:
        return "There was an error sending the request: {}".format(response.errors())

@app.route("/callback", methods=["GET", "POST"])
def callback():
    status = request.args.get("status")
    message = "The request was {}".format(status)
    to = request.args.get("approval_request[transaction][details][Phone Number]")
    resp = client.messages.create(body=message, from_=TWILIO_NUMBER, to=to)
    return resp.sid

@app.route("/push", methods=["GET", "POST"])
def push():
    from_ = request.values.get("From")
    text = request.values.get("Body")

    message = _push(phone=pn.parse(from_), text=text)

    resp = MessagingResponse()
    resp.message(message)

    return str(resp)
