from __future__ import print_function

import time
import gspread
import re
import datetime
import random

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
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage , StickerSendMessage , ImageSendMessage , VideoSendMessage
)

def get_sheet(list_top,list_name,list_target,target):
	# Setup the Sheets API
	SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
	store = file.Storage('credentials.json')
	creds = store.get()
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
		creds = tools.run_flow(flow, store)
	service = build('sheets', 'v4', http=creds.authorize(Http()))

	# Call the Sheets API
	SPREADSHEET_ID = '1F0aMMBcADRSXm07IT2Bxb_h22cIjNXlsCfBYRk53PHA'
	RANGE_NAME = 'A2:G11'
	result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
												 range=RANGE_NAME).execute()
	values = result.get('values', [])
	if not values:
		print('No data found.')
	else:
		sheet_result = "hello world!"
		for row in values:
			# Print columns A and E, which correspond to indices 0 and 4.		
			list_top.append(row[0])
			list_name.append(row[1])
			list_target.append(row[target])
			# print('%s:%s score:%s' % (row[0], row[1] , row[2]))
		

# def post_content():
	
			
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

def update_sheet(gss_client, key, today,messageid,messagetype,text):
    wks = gss_client.open_by_key(key)
    sheet = wks.sheet1
    sheet.insert_row([today,messageid,messagetype,text], 2)


video_list = ["https://i.imgur.com/Upmorh0.mp4"]
image_list = ['https://i.imgur.com/N48r8cd.gif','https://i.imgur.com/iSAnJd4.gif','https://i.imgur.com/8H72aoG.gif','https://i.imgur.com/BTNb7zf.gif','https://i.imgur.com/XO7YFi5.gif','https://i.imgur.com/x0qYhR7.gif']

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

now = datetime.datetime.now()
today = time.strftime("%c")

# print (event.source.userId)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	print(now)
	print(event)	

	user_message = event.message.text
	print (user_message.find("排名"))

	if(user_message== "test"):
		message = TextSendMessage(text='Hello World !!!')
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message== "WC"):
		message = TextSendMessage(text='廁所尻尻')
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message.find("排名") == 0):
		list_top = []
		list_name = []
		list_score = []
		get_sheet(list_top,list_name,list_score,2)
		print (list_top,list_name,list_score)
		score_str = ""
		for i in range(0,10):
			score_str += (str(list_top[i])+"\t"+list_name[i]+"\t"+list_score[i]+"\n")
		print(score_str)
		message = TextSendMessage(text=score_str)
		line_bot_api.reply_message(event.reply_token,message)
		# line_bot_api.push_message(user_id,TextSendMessage(text=score_str))
	elif(user_message.find("褲子") == 0):
		list_top = []
		list_name = []
		list_time = []
		get_sheet(list_top,list_name,list_time,6)
		# print (list_top,list_name,list_score)
		score_str = ""
		score_str += ("目前" + str(list_top[0])+"為\t"+list_name[0]+"\t\n")
		for i in range(1,10):
			score_str += (list_name[i]+"\t還需要 "+list_time[i]+" 才能脫 "+list_name[i-1]+" 的褲子\n")
		print(score_str)
		message = TextSendMessage(text=score_str)
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message == "貼圖辣"):
		randsticker = random.randint(140,180)
		message = StickerSendMessage(package_id='2',sticker_id=str(randsticker))
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message == ("母湯電影版")):		
		message = VideoSendMessage(
		original_content_url='https://i.imgur.com/Upmorh0.mp4',
		preview_image_url='https://i.imgur.com/Upmorh0.gif'
		)
		line_bot_api.reply_message(event.reply_token, message)
	
	elif(user_message.find("母湯") == 0):
		random_pic_i = random.randint(0,len(image_list)-1)
		message = ImageSendMessage(
		original_content_url= image_list[random_pic_i],
		preview_image_url= image_list[random_pic_i]
		)
		line_bot_api.reply_message(event.reply_token, message)
		

	# lineuserid = event.source.userId
	messageid = event.message.id
	# lineuserid = "howard"
	messagetype = event.message.type
	text = event.message.text
	# message = TextSendMessage(text)
	spreadsheet_key = "1Txkvi53ANaFl8Qqug4EsaKTwTGDIgDEarhrewEe2Ruk"	
	# spreadsheet_key_path = 'spreadsheet_key'
	# if cheapest_price is not None:

	# with open(spreadsheet_key_path) as f:
	#    spreadsheet_key = f.read().strip()
	# update_sheet(gss_client, spreadsheet_key, today, messageid,messagetype,text)
	# push message to one user
	# line_bot_api.push_message(user_id, 
	# TextSendMessage(text='Hello World!'))
		
	# line_bot_api.reply_message(
		# event.reply_token,
		# message)
		

		
		
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
