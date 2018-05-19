from __future__ import print_function

import time
import gspread
import re
import datetime
import random
import codecs
import sys
import json

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

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
	MessageEvent, TextMessage, TextSendMessage, ImageSendMessage , 
	StickerSendMessage , ImageSendMessage , VideoSendMessage , TemplateSendMessage,
	SourceUser, SourceGroup, SourceRoom,
	TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
	ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URITemplateAction,
	PostbackTemplateAction, DatetimePickerTemplateAction,
	CarouselTemplate, CarouselColumn, PostbackEvent,
	StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
	ImageMessage, VideoMessage, AudioMessage, FileMessage,
	UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)

# ------ below are self define function ------	
import slient_mode as slient
import switch as switch
import active_mode as active

app = Flask(__name__)
# Channel Access Token
line_bot_api = LineBotApi('+wjG+A6ltvlFVrmQmxyBaXcfljMtYaCTMXnVBoTxhWwMcSRX9+1mMObUO6oVongrp2y7parq1a1/bbbwvOhn/iO26lASkwoWX1u0HBisf7ZRr4cfMzcXFYM/8eFwpeQkdcXYz2obPYl1sE6+kWyC4QdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('4c154ea12f7a284b5edd99087d760143')
# user_id = "Udf8f28a8b752786fa7a6be7d8c808ec6"

now = datetime.datetime.now()

score_sheet_ID = '1F0aMMBcADRSXm07IT2Bxb_h22cIjNXlsCfBYRk53PHA'
my_database_sheet_ID = '1RaGPlEJKQeg_xnUGi1mlUt95-Gc6n-XF_czwudIP5Qk'
april_ID='Udf8f28a8b752786fa7a6be7d8c808ec6'


def readme():
	with open('readme.txt', 'r') as f:
		content = f.read()
	return content
	
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
	print("now: "+str((datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y/%m/%d %H:%M:%S")))
	print("mode: "+str(switch.mode))
	print("event: " +str(event))		
	user_message = event.message.text
	
	if(user_message== "test"):
		message = TextSendMessage(text='Hello World !!!')
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message== "state"):
		message = TextSendMessage(
			text="(silent mode)" if switch.mode == 0 else "(active mode)"
		)
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message in ["!使用說明書","!help","!說明書"]):
		message = TemplateSendMessage(
			alt_text='【使用說明書 ver 2.0】',
			template=CarouselTemplate(
				columns=[
					CarouselColumn(
						thumbnail_image_url='https://i.imgur.com/02b6MnB.jpg',
						title=' - 【使用說明書】 - ',
						text='!使用說明書、!help、!說明書',
						actions=[
							PostbackTemplateAction(
								label='說明書',
								text='!使用說明書',
								data='action=buy&itemid=1'
							),
							MessageTemplateAction(
								label='test',
								text='!使用說明書'
							),
							# URITemplateAction(
							# 	label='uri1',
							# 	uri='http://example.com/1'
							# )
						]
					),
					CarouselColumn(
						thumbnail_image_url='https://i.imgur.com/02b6MnB.jpg',
						title=' - 【維修智乃類】 - ',
						text='!壞掉啦、呼叫四月、呼叫工程師',
						actions=[
							PostbackTemplateAction(
								label='呼叫四月',
								text='呼叫四月',
								data='action=buy&itemid=1'
							),
							MessageTemplateAction(
								label='呼叫工程師',
								text='呼叫工程師'
							),
							# URITemplateAction(
							# 	label='uri1',
							# 	uri='http://example.com/1'
							# )
						]
					),
					CarouselColumn(
						thumbnail_image_url='https://i.imgur.com/02b6MnB.jpg',
						title=' - 【主要開關類】 -',
						text='!開關',
						actions=[
							PostbackTemplateAction(
								label='讓智乃說話',
								text='!說話',
								data='action=buy&itemid=1'
							),
							MessageTemplateAction(
								label='請智乃閉嘴',
								text='!閉嘴'
							),
							# URITemplateAction(
							# 	label='uri1',
							# 	uri='http://example.com/1'
							# )
						]
					),
					CarouselColumn(
						thumbnail_image_url='https://i.imgur.com/02b6MnB.jpg',
						title=' - 【健康教育類】 - ',
						text='!教育/調教、!智乃看圖片、!給智乃看圖、!智乃看圖圖、〖修復中〗!忘記',
						actions=[
							PostbackTemplateAction(
								label='test',
								text='test',
								data='action=buy&itemid=1'
							),
							MessageTemplateAction(
								label='test',
								text='test'
							),
							# URITemplateAction(
							# 	label='uri1',
							# 	uri='http://example.com/1'
							# )
						]
					),
					CarouselColumn(
						thumbnail_image_url='https://i.imgur.com/02b6MnB.jpg',
						title=' - 【算命抽籤類】 - ',
						text='!機率、!抽數字',
						actions=[
							PPostbackTemplateAction(
								label='test',
								text='test',
								data='action=buy&itemid=1'
							),
							MessageTemplateAction(
								label='test',
								text='test'
							),
							# URITemplateAction(
							# 	label='uri1',
							# 	uri='http://example.com/1'
							# )
						]
					),
					CarouselColumn(
						thumbnail_image_url='https://i.imgur.com/02b6MnB.jpg',
						title=' - 【遊戲抽抽類】 - ',
						text='!抽抽、!終極密碼、!幾A幾B、小遊戲、機會命運',
						actions=[
							PostbackTemplateAction(
								label='test',
								text='test',
								data='action=buy&itemid=1'
							),
							MessageTemplateAction(
								label='test',
								text='test'
							),
							# URITemplateAction(
							# 	label='uri1',
							# 	uri='http://example.com/1'
							# )
						]
					),
					CarouselColumn(
						thumbnail_image_url='https://i.imgur.com/02b6MnB.jpg',
						title=' - 【不知幹嘛類】 - ',
						text='貼圖辣、母湯、母湯電影版',
						actions=[
							PostbackTemplateAction(
								label='test',
								text='test',
								data='action=buy&itemid=1'
							),
							MessageTemplateAction(
								label='test',
								text='test'
							),
							# URITemplateAction(
							# 	label='uri1',
							# 	uri='http://example.com/1'
							# )
						]
					),
					CarouselColumn(
						thumbnail_image_url='https://i.imgur.com/02b6MnB.jpg',
						title=' - 【散步打排名 1】 - ',
						text='即時排名/即時戰況/排名/分數/戰況/score、%數/%、一位差、分數差',
						actions=[
							PostbackTemplateAction(
								label='test',
								text='test',
								data='action=buy&itemid=1'
							),
							MessageTemplateAction(
								label='test',
								text='test'
							),
							# URITemplateAction(
							# 	label='uri1',
							# 	uri='http://example.com/1'
							# )
						]
					),
					CarouselColumn(
						thumbnail_image_url='https://i.imgur.com/02b6MnB.jpg',
						title=' - 【散步打排名 2】 - ',
						text='場數差、追擊時間/脫褲子、時速、場速、活動進度/進度、剩餘時間',
						actions=[
							PostbackTemplateAction(
								label='test',
								text='test',
								data='action=buy&itemid=1'
							),
							MessageTemplateAction(
								label='test',
								text='test'
							),
							# URITemplateAction(
							# 	label='uri1',
							# 	uri='http://example.com/1'
							# )
						]
					),
					CarouselColumn(
						thumbnail_image_url='https://i.imgur.com/02b6MnB.jpg',
						title=' - 【散步打排名 3】 - ',
						text='房號/room/rm/R/r、r1/room1、r2/room2',
						actions=[
							PostbackTemplateAction(
								label='test',
								text='test',
								data='action=buy&itemid=1'
							),
							MessageTemplateAction(
								label='test',
								text='test'
							),
							# URITemplateAction(
							# 	label='uri1',
							# 	uri='http://example.com/1'
							# )
						]
					)
				]
			)
		)
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message in ["!getinfo"]):
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text=str(event)))
	elif(user_message in ["!壞掉啦","呼叫工程師","呼叫四月"]):
		line_bot_api.push_message(april_ID, TextSendMessage(text='智乃壞掉囉~~~'))
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已經幫您通知拔拔了! 請稍等~~"))
	elif(user_message== "!重新開機" or user_message == "!restart"):
		message = TextSendMessage(text="restarting...")
		line_bot_api.reply_message(event.reply_token,message)
		sys.exit(0)
	elif(switch.mode == 0):
		message = slient.slient_mode(user_message,event) 
		line_bot_api.reply_message(event.reply_token,message)
	elif(switch.mode == 1):
		active.active_mode(user_message,event)
		
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

