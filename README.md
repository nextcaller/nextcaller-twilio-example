nextcaller-twilio-example-python
================================

This project demonstrates usage of the Twilio SDK and Next Caller AddOn for Voice Calls.

When the configured Twilio number is called, an SMS will be sent to the designated target number with details about the caller.

Installation
------------

*Requirements:*

* Twilio account (https://www.twilio.com/try-twilio)
  - Allocated phone number (https://www.twilio.com/console/phone-numbers/)
  - Next Caller AddOn instgalled and enabled for Incoming Voice Callls (https://www.twilio.com/console/add-ons/XB73cdb5ac3395a439800f298fa8a43f02)

* Heroku account (https://signup.heroku.com/)

*Clone the GitHub Repository and Create the Heroku Project:*

    $ git clone git://github.com/nextcaller/nextcaller-twilio-example-python.git
    $ cd nextcaller-twilio-example-python
    $ heroku login
    $ heroku create # Note application URL
    $ git push heroku master


*Heroku Variables:*

* `SMS_FROM` - Phone number allocated above
* `SMS_TO` - An SMS enabled device or number
* `TWILIO_SID` - SID for the Twilio account to use
* `TWILIO_TOKEN` - Token for the Twilio account to use

*Set Variables:*

    $ heroku config:set SMS_FROM='+15055551212' SMS_TO='+14045551212' TWILIO_SID='ABC...' TWILIO_TOKEN='10f...'


*Configure Twilio Phone Number:*

From the Twilio phone numbers page (https://www.twilio.com/console/phone-numbers/), select the number to configure and enter the application URL (noted above) as the Webhook (POST method).

*Testing:*

To test the application, call the Twilio phone number. You should receive an SMS on the `SMS_TO` device. The message will include the caller's name, gender, and marital status.
