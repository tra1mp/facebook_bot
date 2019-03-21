import random
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'EAAENolH3AzgBAFHTYqW6B7N5WXFVeLFEqxtSCi0bZBA4VSVWxRh5ZBNM8uPc5U2ZArZCVkCNVkPkZC2Kaet0e0XHJrzF1YAMJqFKx0KAA1X16YZANLzw8DSoYVjlYt5hjdG5SUyyHF59qvlq5TtS1QPEzEfeaUqvwycNGqPCErKKzZAaK4U0ZBbl'
VERIFY_TOKEN = 'SECRET'
bot = Bot(ACCESS_TOKEN)

#Получать сообщения, посылаемые фейсбуком нашему боту мы будем в этом терминале
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        #до того как позволить людям отправлять что-либо боту, Facebook проверяет токен,
    # подтверждающий, что все запросы, получаемые ботом, приходят из Facebook 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #если запрос не был GET, это был POST-запрос и мы обрабатываем запрос пользователя
    else:
        # получаем сообщение, отправленное пользователем для бота в Facebook
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
               #определяем ID, чтобы знать куда отправлять ответ
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = get_message()
                    send_message(recipient_id, response_sent_text)
                #если пользователь отправил GIF, фото, видео и любой не текстовый объект
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
   #'''Сверяет токен, отправленный фейсбуком, с имеющимся у вас.
    #При соответствии позволяет осуществить запрос, в обратном случае выдает ошибку.'''
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#Выбирает случайное сообщение и отправляет пользователю
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    #'''Отправляет случайные сообщения пользователю.'''
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #'''Отправляет пользователю текстовое сообщение в соответствии с параметром response.'''
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()
