from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

# create app
app = Flask(__name__)
with open('channel_access_token') as fi:
    text = fi.read().split('\n')
    cat = text[0]
    secret = text[1]
line_bot_api = LineBotApi(cat)
handler = WebhookHandler(secret)

# import wrapper
from wrapper import predict

@app.route("/elur_test", methods=['GET'])
def elur_test():
    sentence = 'Apa sih, ga lucu'
    emo = predict(sentence)
    return emo

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    text = event.message.text
    emo = predict(text)

    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text="Predicted emotion: {}".format(emo)))



if __name__ == "__main__":
    app.run()