from flask import Flask, Response, request

app = Flask(__name__)

app.config.from_object('app_config')


@app.route("/sms", methods=["GET", "POST"])
def sms():
    from_number = request.values.get("From")
    incoming_message = request.values.get("Body", "").encode("utf-8")

    twiml = """
    <Response>
        <Message>
            Hello! I see you're texting me from: {}\n\nHere's the message I received:\n\n{}
        </Message>
    </Response>
    """.format(from_number, incoming_message)

    return Response(twiml, mimetype="text/xml")


if __name__ == '__main__':
    app.run()
