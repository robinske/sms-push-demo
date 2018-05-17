import os
import random
import phonenumbers as pn

from flask import Flask, Response, request

from authy.api import AuthyApiClient

authy_api = AuthyApiClient(os.environ["PUSH_DEMO_AUTHY_API_KEY"])

## # TODO:
# Add logo, details, more info in general


app = Flask(__name__)

def _push(phone, text):
    country_code = phone.country_code
    number = phone.national_number

    user = authy_api.users.create(
        'stub@myemail.com',
        number,
        country_code)

    logo = {
        'res': 'default',
        'url': 'https://github.com/robinske/sms-push-demo/blob/master/wave.png?raw=true'
    }

    details = {
        'Account Number': str(user.id),
        'Phone Number': str(number)
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
        return response.get_uuid()
    else:
        return "There was an error sending the request: {}".format(response.errors())

@app.route("/action", methods=["GET", "POST"])
def action():
    # use as webhook to send notification about whether it was accepted or rejected
    pass

@app.route("/push", methods=["GET", "POST"])
def push():
    from_ = request.values.get("From")
    message_ = request.values.get("Body")

    uuid = _push(phone=pn.parse(from_), text=message_)

    twiml = """
    <Response>
        <Message>
            Push notification incoming!
        </Message>
    </Response>
    """

    return Response(twiml, mimetype="text/xml")
