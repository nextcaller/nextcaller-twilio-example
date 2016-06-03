import os
import json
from flask import Flask, request
import twilio.twiml
from twilio.rest import TwilioRestClient

app = Flask(__name__)


# Retrieve environment variables set by Heroku
account_sid = os.environ['TWILIO_SID']
auth_token = os.environ['TWILIO_TOKEN']
message_target = os.environ['SMS_TO']
cid = os.environ['SMS_FROM']


@app.route("/", methods=['POST'])
def respond():
    from_number = request.values.get('From', None)

    # Extract the Next Caller AddOn results
    try:
        addons = json.loads(request.values.get('AddOns', '{}'))
        next_caller = addons['results']['nextcaller_advanced_caller_id']
    except KeyError:
        next_caller = None

    resp = twilio.twiml.Response()

    if not next_caller:
        print('Next Caller AddOn not enabled')
        resp.hangup()
        return str(resp)
    elif next_caller['status'] != 'successful':
        print 'Next Caller lookup failed'
        resp.hangup()
        return str(resp)

    records = next_caller['result']['records']

    if not records:
        print 'No Next Caller match found'
        resp.hangup()
        return str(resp)

    caller = records[0]

    fname = caller.get('first_name')
    name = caller.get('name') or 'Anonymous'
    gender = caller.get('gender') or'Unknown Gender'
    marital_status = caller.get('marital_status') or '?'
    phones = caller.get('phone')

    if phones:
        linetype = phones[0].get('line_type')
    else:
        linetype = None

    # Greet the caller by name and tell them the type of phone they're
    # calling form (mobile or landline).
    greet = 'Hi, anonymous caller!'

    if name:
        greet = 'Hi, {}!'.format(fname)

    if linetype:
        greet = greet + ' You are calling from a {} phone.'.format(linetype)

    resp.say(greet)

    # Send an SMS to the configured address with info about the caller
    body = 'Call from {}: {} ({} / {}).'.format(from_number, name,
                                                marital_status, gender)
    client = TwilioRestClient(account_sid, auth_token)
    client.messages.create(to=message_target, from_=cid, body=body)

    return str(resp)

if __name__ == "__main__":
    # PORT is set by Heroku
    port = int(os.environ.get('PORT', 8080))
    print "starting on port {}".format(port)
    app.run(debug=True, host='0.0.0.0', port=port)
