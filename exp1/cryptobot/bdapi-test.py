from tokens import cmc_token
from datetime import date

import requests,json,re,os
from flask import Flask,request,Response

token = os.getenv('cmc_botoken')
app = Flask(__name__)
today = date.today()
t = today.strftime("%m-%d")
commands = ['BDAYFAM','BDAYFRIENDS','COMMANDS']


def write_json(data,filename='response.json'):
    with open(filename, 'w') as f:
        json.dump(data,f,indent=4, ensure_ascii=False)


def get_data(symbol):
    url = 'http://127.0.0.1:8000/api/all'

    req = requests.get(url).json()
    respfa = []
    respfr = []
    bdhumans = ""


    for human in req :
        if human['category'] == 'family':
            l = human['human_dob'][5:]
            if l == t :
                respfa.append(human['human_name'])
        else :
            l = human['human_dob'][5:]
            if l == t :
                respfr.append(human['human_name'])


    if symbol == commands[0]:
        if len(respfa) == 0:
            return "No Birthdays today"
        else :
            for bdp in respfa:
                bdhumans += str(bdp)
                bdhumans += "\n"
        
        return bdhumans
    elif symbol == commands[1]:
        if len(respfr) == 0:
            return "No Birthdays today"
        else :
            for bdp in respfr:
                bdhumans += str(bdp)
                bdhumans += "\n"
        return bdhumans        
    elif symbol == commands[2]:
        return "1./bdayfam --> Family birthday events\n2./bdayfriends --> Friends birthday event\n3./commands --> list commands"




    # https://api.telegram.org/bot{token}/sendMessage?chat_id=1342633095&text=Text

    # https://api.telegram.org/bot{token}/setWebhook?url=https://proud-rattlesnake-27.loca.lt


def parse_message(message):
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']  # /gb /btc

    pattern = r'/[a-zA-Z]{2,15}'

    ticker = re.findall(pattern, txt)

    if ticker :
        symbol = ticker[0][1:].upper()  # /gb > gb  can also use .strip('/')
        if symbol not in commands:
            symbol = ''
    else:
        symbol = ''

    return chat_id,symbol


def send_message(chat_id, text='bla-bla=bla'):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload  = { 'chat_id':chat_id, 'text': text}

    r = requests.post(url,json=payload)
    return r


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id,symbol = parse_message(msg)

        if not symbol:
            send_message(chat_id,'Wrong data')
            write_json(msg, 'telegram_request.json')
            return Response('ok', status=200)


        bday = get_data(symbol)
        write_json(msg, 'telegram_request.json')
        send_message(chat_id,bday)
        return Response('ok', status=200)

    else:
        return '<h1>CMCBOT</h1>\nMaking sure that webhook is set and backend is running'


def main():
    print("MAIN")


if __name__ == '__main__':
    #main()
    app.run(debug=True)


