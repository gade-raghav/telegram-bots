                                                                                                                                                                                                                                                                                                                                                                                                                        
import requests,json,re,os                                                                                                                                        
from flask import Flask,request,Response                                                                                                                          
from flask_sslify import SSLify                                                                                                                                   
from datetime import date                                                                                                                                         
                                                                                                                                                                  
token = os.getenv('botoken')                                                                                                                                      
app = Flask(__name__)                                                                                                                                             
sslify = SSLify(app)                                                                                                                                              
today = date.today()                                                                                                                                              
t = today.strftime("%m-%d")                                                                                                                                       
commands = ['BDAYFAM','BDAYFRIENDS','COMMANDS','SET','START']                                                                                                     
                                                                                                                                                                  
                                                                                                                                                                  
def write_json(data,filename='response.json'):                                                                                                                    
    with open(filename, 'w') as f:                                                                                                                                
        json.dump(data,f,indent=4, ensure_ascii=False)                                                                                                            
                                                                                                                                                                  
                                                                                                                                                                 
def get_data(symbol,data=''):
    #Changes when api is exposed on different webserver. Add a local variable .bashrc to make stuff easier.  
    urlc = 'http://9f7abd833b20.ngrok.io/api/create/'                                                                                                        
    url = 'http://9f7abd833b20.ngrok.io/api/all/'                                                                                                                 
                                                                                                                                                                  
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
        cmdfa = 'echo '+bdhumans+' >bdfams.log '
        os.system(cmdfa) 
        return bdhumans
    elif symbol == commands[1]:
        if len(respfr) == 0:
            return "No Birthdays today"
        else :
            for bdp in respfr:
                bdhumans += str(bdp)
                bdhumans += "\n"
        cmdfr = 'echo '+bdhumans+' >>bdfriends.log '
        os.system(cmdfr)
        return bdhumans        
    elif symbol == commands[3]:
        cmd  = 'curl --data "'+data+'" '+urlc+' 2>error.log'
        statuscode = os.system(cmd)
        if statuscode == 0 :
            return  "We've taken your post request, and we'll add it to our DB :)"
        else :
            return "Please enter the data as given in the /set command format"
    elif symbol == commands[2]:
        return  '1./bdayfam --> Family birthday events\n2./bdayfriends --> Friends birthday event\n3./commands --> list commands\n4.Post request format as follows:\n/set human_name=YOURNAME&human_dob=YYYY-MM-DD&human_gender=male/female/other&category=friends/family ' 
    elif symbol == commands[4]:
        return 'Welcome to BDBOT_GI. Report issues on https://github.com/gade-raghav/telegram-bots (also tag bot name while mentioning issues :). /commands for all bot commands. Sayonara.'
    else :
        return "Working"
    #SENDMESSAGE_URL_TELEGRAM https://api.telegram.org/bot{token}/sendMessage?chat_id=1342633095&text=Text
    #SETWEBHOOK_URL_TELEGRAMi https://api.telegram.org/bot{token}/setWebhook?url=https://proud-rattlesnake-27.loca.lt
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
    data= ""
    if request.method == 'POST':
        msg = request.get_json()
        chat_id,symbol = parse_message(msg)
        if not symbol:
            send_message(chat_id,'No such command :( \nUse /commands to get list of commands :)')
            #write_json(msg, 'telegram_request.json')
            return Response('ok', status=200)
        elif symbol == "SET" :
            data=msg['message']['text'][5:]
        bday = get_data(symbol,data)
        #write_json(bday, 'telegram_request.json')
        send_message(chat_id,bday)
        return Response('ok', status=200)
    else:
        return '<h1>BDBOT_GI</h1>\n<h4>Backend check. OK-OK COOL COOL</h4>\nEnter BDBOT_GI in telegram and feel free to send commands ;) <footer><a href="https://gade-raghav.github.io/about" target="blank">Raghav Gade</a></footer>'
def main():
    print("Test-DEMO")
if __name__ == '__main__':
    #main()
    app.run(debug=True)
