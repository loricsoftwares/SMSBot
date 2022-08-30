from flask import Flask,request
import json
import requests
from twilio.base.exceptions import TwilioRestException

from twilio.rest import Client
import os

import time

account_sid = 'AC785d1794381de9f462102d62e825b13e'
auth_token = 'c927adfaa2b05993578e87b694a318bd'


teleToken = '5637244545:AAGKg3N423djivE6VNwqQIi8E1T3BUEklgg'

app = Flask(__name__)
app.debug =True

client = Client(account_sid, auth_token)

option_selected = "-1"

print("Printing..")


def parse_message(message):
    chat_id = message['message']['chat']['id']
    text = message['message']['text']

    return chat_id,text

def send_message(chat_id,text="bla-bla-bla"):
    url = f'https://api.telegram.org/bot{teleToken}/sendMessage'
    payload = {'chat_id':chat_id,'text':text}

    r = requests.post(url,json=payload)

    return r

def send_sms(phone_no,text):

    try:
        message = client.messages.create(
            messaging_service_sid='MG9e315183fb3f0408175a3c899daa2990',
            body=''+str(text),
            to='91'+str(phone_no)
        )
        return message.status
    except TwilioRestException as e:
          send_message(890250748,e)



def write_json(data,filename='response.json'):
    with open(filename,'w') as f:
        json.dump(data,f,indent=4,ensure_ascii=False)


@app.route('/',methods=['POST'])
def index():
    global option_selected
    if request.method =='POST':
        msg = request.get_json()

        chat_id,text = parse_message(msg)


        textLen = len(str(text))

        if str(text) =="/start":
            send_message(chat_id,"Welcome to Loric's BOT, follow the below option to use it. Use it with your own risk.")
            send_message(chat_id,"1.Send Custom SMS\n2.Call Bomber\n3.Automated Call")
            send_message(chat_id,"Reply with (1, 2 or 3) :")
        if str(text) =="1":
                option_selected = "1"
                send_message(chat_id,"reply with (phone,message) :")
        if(textLen>10):

            phoneNumberHai = str(text)[0:10]
            messageHai =str(text)[11:textLen]

            send_message(chat_id,"got the ans:"+phoneNumberHai)
            send_message(chat_id,"got the ans:"+messageHai)

            if(option_selected=="1" and textLen>10 ):
                ress = send_sms(""+phoneNumberHai,""+messageHai)
                send_message(890250748,"Message Sended Sucessfully"+ress)
                option_selected="-1"
            if(option_selected=="2" and textLen>10 ):
                print("Second option selected")
                send_message(890250748,"Calling..")
                try:
                    call = client.calls.create(
                    twiml='<Response><Say voice="Polly.Aditi">'+messageHai+'</Say></Response>',
                    to='+91'+phoneNumberHai,
                    from_='+15312332632'
                    )
                    print(call.sid)
                    send_message(890250748,""+call.sid)
                except TwilioRestException as e:
                      send_message(890250748,"Error "+e)

        if str(text) == "2":
            option_selected = "2"
            send_message(chat_id,"You have selected 2")
        if str(text) == "3":
            send_message(chat_id,"You have selected 3")

        return 'ok',200
    else:
        print("sdaddda")
        return 'Hello'



if __name__ == "__main__":
    app.run(debug=True)






#https://api.telegram.org/bot5637244545:AAGKg3N423djivE6VNwqQIi8E1T3BUEklgg/sendMessage?chat_id=&text=Hello
#https://api.telegram.org/bot5637244545:AAGKg3N423djivE6VNwqQIi8E1T3BUEklgg/sendMessage?chat_id=5637244545&text=Hello