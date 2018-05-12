import time
import gspread
import re
import datetime
import random

from flask import Flask, request, abort
from urllib.request import urlopen
from oauth2client.service_account import ServiceAccountCredentials

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage , StickerSendMessage
)

def auth_gss_client(path, scopes):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(path,scopes)
    return gspread.authorize(credentials)

 
app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('+wjG+A6ltvlFVrmQmxyBaXcfljMtYaCTMXnVBoTxhWwMcSRX9+1mMObUO6oVongrp2y7parq1a1/bbbwvOhn/iO26lASkwoWX1u0HBisf7ZRr4cfMzcXFYM/8eFwpeQkdcXYz2obPYl1sE6+kWyC4QdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('4c154ea12f7a284b5edd99087d760143')
user_id = "Udf8f28a8b752786fa7a6be7d8c808ec6"

auth_json_path = "./auth.json"

gss_scopes = ['https://spreadsheets.google.com/feeds']



gss_client = auth_gss_client(auth_json_path, gss_scopes)

def update_sheet(gss_client, key, today,text):
    wks = gss_client.open_by_key(key)
    sheet = wks.sheet1
    sheet.insert_row([today,"test"], 2)



# update.py
		
#push message to one user
# line_bot_api.push_message(user_id, 
    # TextSendMessage(text='Hello World!'))
# push message to multiple users
# line_bot_api.multicast(['user_id1', 'user_id2'], 
    # TextSendMessage(text='Hello World!'))	
	
	
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
	if(event.message.text== "abc"):
		message = TextSendMessage(text='Hello')
	elif(event.message.text== "貼圖辣"):
		randsticker = random.randint(140,180)
		message = StickerSendMessage(
		package_id='2',
		sticker_id=str(randsticker)
		)
	else:
		message = TextSendMessage(text=event.message.text)
		spreadsheet_key = "19nQvlQIGRIoGELFxGfHWazG45DM7D2GccZg8wlD85_g"	
		# spreadsheet_key_path = 'spreadsheet_key'
		now = datetime.datetime.now()

		# if cheapest_price is not None:
		today = time.strftime("%c")
		# with open(spreadsheet_key_path) as f:
		#    spreadsheet_key = f.read().strip()
		update_sheet(gss_client, spreadsheet_key, today, message)
	#push message to one user
	line_bot_api.push_message(user_id, 
	TextSendMessage(text='Hello World!'))
		
	line_bot_api.reply_message(
		event.reply_token,
		message)
		

		
		
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
