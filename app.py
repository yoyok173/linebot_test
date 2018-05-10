from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('+wjG+A6ltvlFVrmQmxyBaXcfljMtYaCTMXnVBoTxhWwMcSRX9+1mMObUO6oVongrp2y7parq1a1/bbbwvOhn/iO26lASkwoWX1u0HBisf7ZRr4cfMzcXFYM/8eFwpeQkdcXYz2obPYl1sE6+kWyC4QdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('4c154ea12f7a284b5edd99087d760143')

# 監聽所有來自 /callback 的 Post Request
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
	usertext = event.message.text
	# if (text == "eyny"):
        # content = "eyny"
        # line_bot_api.reply_message(
            # event.reply_token,
            # TextSendMessage(text=content))
        # return 0
		
	# else:
	message222 = TextSendMessage(text=usertext)		
	line_bot_api.reply_message(event.reply_token, message222)

	
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
