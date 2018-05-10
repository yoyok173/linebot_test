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
	if event.message.text == "eyny":
        content = "eyny"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
	else:
		message = TextSendMessage(text=event.message.text)		
		line_bot_api.reply_message(event.reply_token, message)

	# if event.message.text == "貼圖":
		# message = StickerSendMessage(
			# package_id='1',
			# sticker_id='1'	
		# )
	# if event.message.text == "表":
        # message = TemplateSendMessage(
            # alt_text='開始玩 template',
            # template=ButtonsTemplate(
                # title='選擇服務',
                # text='請選擇',
                # thumbnail_image_url='https://i.imgur.com/xQF5dZT.jpg',
                # actions=[
                    # MessageTemplateAction(
                        # label='新聞',
                        # text='新聞'
                    # ),
                    # MessageTemplateAction(
                        # label='電影',
                        # text='電影'
                    # ),
                    # MessageTemplateAction(
                        # label='看廢文',
                        # text='看廢文'
                    # ),
                    # MessageTemplateAction(
                        # label='正妹',
                        # text='正妹'
                    # )
                # ]
            # )
        # )
	# if(event.message.text="抽"):
		# image = requests.get(API_Get_Image)
        # url = image.json().get('Url')
        # message = ImageSendMessage(
            # original_content_url=url,
            # preview_image_url=url
        # )
	# else:

	
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
