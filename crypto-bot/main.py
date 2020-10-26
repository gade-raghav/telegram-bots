from tokens import cmc_token
import requests,json,re,os
from flask import Flask,request,Response
token = os.getenv('cmc_botoken')
app = Flask(__name__)



def write_json(data,filename='response.json'):
    with open(filename, 'w') as f:
        json.dump(data,f,indent=4, ensure_ascii=False)


def get_data(crypto):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

    params = {'symbol': crypto, 'convert':'USD'}
    headers = {'X-CMC_PRO_API_KEY': cmc_token}

    req = requests.get(url,headers=headers,params=params).json()
    price = req['data'][crypto]['quote']['USD']['price']
    return price

    # https://api.telegram.org/bot{token}/sendMessage?chat_id=1342633095&text=Text

    # https://api.telegram.org/bot{token}/setWebhook?url=https://proud-rattlesnake-27.loca.lt


def parse_message(message):
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']  # /gb /btc

    pattern = r'/[a-zA-Z]{2,4}'

    ticker = re.findall(pattern, txt)

    if ticker :
        symbol = ticker[0][1:].upper()  # /gb > gb  can also use .strip('/')
        if symbol != 'BTC':
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


        price = get_data(symbol)
        write_json(msg, 'telegram_request.json')
        send_message(chat_id,price)

        return Response('ok', status=200)
    else:
        return '<h1>CMCBOT</h1>'


def main():
    print(get_data('BTC'))


if __name__ == '__main__':
    # main()
    app.run(debug=True)


