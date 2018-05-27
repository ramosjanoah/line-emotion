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

app = Flask(__name__)

with open('channel_access_token') as fi:
	text = fi.read().split('\n')
	cat = text[0]
	secret = text[1]

print(cat)
print(secret)

line_bot_api = LineBotApi(cat)
handler = WebhookHandler(secret)

@app.route("/darling", methods=['GET'])
def darling():
	text = "Oh darling, your request is {}<br>".format(request)
	text += "LINE BOT API : {}<br>".format(line_bot_api)
	text += "Secret[0:10] : {}<br>".format(secret[0:10])
	return text

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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="Apapun yang kamu katakan, aku akan reply pake pesan ini."))


if __name__ == "__main__":
    app.run()