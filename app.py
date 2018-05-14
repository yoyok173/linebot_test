from __future__ import print_function

import time
import gspread
import re
import datetime
import random
import codecs
import sys

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

# video_list = ["https://i.imgur.com/Upmorh0.mp4"]
# image_list = ['https://i.imgur.com/N48r8cd.gif','https://i.imgur.com/iSAnJd4.gif','https://i.imgur.com/8H72aoG.gif','https://i.imgur.com/BTNb7zf.gif','https://i.imgur.com/XO7YFi5.gif','https://i.imgur.com/x0qYhR7.gif']

BGD_namelist = [
'牛込りみ','山吹沙綾','戸山香澄','市ヶ谷有咲','花園たえ',
'上原ひまり','羽沢つぐみ','美竹蘭','宇田川巴','青葉モカ',
'白鷺千聖','若宮イヴ','丸山彩','大和麻弥','氷川日菜',
'氷川紗夜','宇田川あこ','湊友希那','白金燐子','今井リサ',
'北沢はぐみ','奥沢美咲','弦巻こころ','瀬田薫','松原花音']

SC_nameList = [
'風野灯織','八宮めぐる','櫻木真乃','月岡恋鐘',
'田中摩美々','幽谷霧子','三峰結華','白瀬咲耶',
'桑山千雪','大崎甘奈','大崎甜花','小宮果穂',
'杜野凛世','園田智代子','西城樹里','有栖川夏葉'
]



app = Flask(__name__)
# Channel Access Token
line_bot_api = LineBotApi('+wjG+A6ltvlFVrmQmxyBaXcfljMtYaCTMXnVBoTxhWwMcSRX9+1mMObUO6oVongrp2y7parq1a1/bbbwvOhn/iO26lASkwoWX1u0HBisf7ZRr4cfMzcXFYM/8eFwpeQkdcXYz2obPYl1sE6+kWyC4QdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('4c154ea12f7a284b5edd99087d760143')
# user_id = "Udf8f28a8b752786fa7a6be7d8c808ec6"
auth_json_path = "./auth.json"

now = datetime.datetime.now()
today = time.strftime("%c")
mode = 1

# game SSR Prob
SC_SSR_P_prob = 20 # SC Produce idol SSR_probability
SC_SSR_S_prob = 30 # SC Support idol SSR_probability
SC_SR_P_prob = 60 # SC Produce idol SR_probability
SC_SR_S_prob = 100 # SC Support idol SR_probability
SC_R_R_prob = 290 # SC Support idol R_probability

def get_score_sheet(list_top,list_name,list_target,target):
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
	RANGE_NAME = 'A2:M11'
	result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
												 range=RANGE_NAME).execute()
	values = result.get('values', [])
	if not values:
		print('No data found.')
	else:
		for row in values:	
			list_top.append(row[0])
			list_name.append(row[1])
			list_target.append(row[target])
		
def get_key_response(key):
	# Setup the Sheets API
	SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
	store = file.Storage('credentials.json')
	creds = store.get()
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
		creds = tools.run_flow(flow, store)
	service = build('sheets', 'v4', http=creds.authorize(Http()))

	# Call the Sheets API
	SPREADSHEET_ID = '1RaGPlEJKQeg_xnUGi1mlUt95-Gc6n-XF_czwudIP5Qk'
	RANGE_NAME = 'Sheet1!A2:B2000'
	result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
												 range=RANGE_NAME).execute()
	values = result.get('values', [])
	if not values:
		print('No data found.')
	else:
		list_key = []
		list_response = []
		for row in values:	
			list_key.append(row[0])
			list_response.append(row[1])
		if key in list_key:
			# list_response = list_key.index(key)
			list_response_index = [i for i,v in enumerate(list_key) if v==key]
			print (list_response_index)
			random_reply = random.randint(0,len(list_response_index)-1)
			return list_response[list_response_index[random_reply]]
		else:
			return 0
		
def auth_gss_client(path, scopes):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(path,scopes)
    return gspread.authorize(credentials)

gss_scopes = ['https://spreadsheets.google.com/feeds']
gss_client = auth_gss_client(auth_json_path, gss_scopes)

def update_sheet(gss_client, key, today,messageid,messagetype,text):
    wks = gss_client.open_by_key(key)
    sheet = wks.sheet1
    sheet.insert_row([today,messageid,messagetype,text], 2)
	
def update_sheet_key(gss_client, key, input , output):
    wks = gss_client.open_by_key(key)
    sheet = wks.sheet1
    sheet.insert_row([input , output], 2)
	
def get_food_sheet(key):
	# Setup the Sheets API
	SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
	store = file.Storage('credentials.json')
	creds = store.get()
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
		creds = tools.run_flow(flow, store)
	service = build('sheets', 'v4', http=creds.authorize(Http()))

	# Call the Sheets API
	SPREADSHEET_ID = '1RaGPlEJKQeg_xnUGi1mlUt95-Gc6n-XF_czwudIP5Qk'
	if key == 1:
		RANGE_NAME = 'food!A2:A'
	elif key == 2:
		RANGE_NAME = 'food!B2:B'
	result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
												 range=RANGE_NAME).execute()
	values = result.get('values', [])
	if not values:
		print('No data found.')
	else:
		list_food = []
		for row in values:	
			list_food.append(row[0])
			
		random_food_index = random.randint(0,len(list_food)-1)
		return list_food[random_food_index]

def gacha_BGD():
	random_number = random.randint(0,999)
	if random_number < 30:
		return "4★ "+random.choice(BGD_namelist)
	elif random_number < 30+85:
		return "3★ "+random.choice(BGD_namelist)
	elif random_number < 30+85+885:
		return "2★ "+random.choice(BGD_namelist)
	
def gacha_last_BGD():
	random_number = random.randint(0,99)
	if random_number < 3:
		return "4★ "+random.choice(BGD_namelist)
	elif random_number < 3+97:
		return "3★ "+random.choice(BGD_namelist)
	
def ten_gacha_BGD():
	ten_gacha_BGD_result=""
	for i in range(9):
		ten_gacha_BGD_result += str(gacha_BGD())
		ten_gacha_BGD_result += "\n"
	ten_gacha_BGD_result += str(gacha_last_BGD())
	return ten_gacha_BGD_result
	
def gacha_CGSS():
	random_number = random.randint(0,99)
	if random_number < 3:
		return "SSR"
	elif random_number < 3+12:
		return "SR"
	elif random_number < 3+12+85:
		return "R"
	
def gacha_last_CGSS():
	random_number = random.randint(0,99)
	if random_number < 3:
		return "SSR"
	elif random_number < 3+97:
		return "SR"
	
def ten_gacha_CGSS():	
	ten_gacha_CGSS_result=""
	for i in range(9):
		ten_gacha_CGSS_result += str(gacha_CGSS())
		if i == 4:
			ten_gacha_CGSS_result += "\n"
		else:
			ten_gacha_CGSS_result += " , "
	ten_gacha_CGSS_result += str(gacha_last_CGSS())
	return ten_gacha_CGSS_result
	
def gacha_SC():
	global SC_SSR_P_prob, SC_SSR_S_prob, SC_SR_P_prob, SC_SR_S_prob
	rand = random.randint(0,999)
	if rand < SC_SSR_P_prob:
		return "[P] SSR"
	elif rand < (SC_SSR_P_prob + SC_SSR_S_prob):
		return "[S] SSR"
	elif rand < (SC_SSR_P_prob + SC_SSR_S_prob + SC_SR_P_prob):
		return "[P] SR"
	elif rand < (SC_SSR_P_prob + SC_SSR_S_prob + SC_SR_P_prob + SC_SR_S_prob):
		return "[S] SR"
	elif rand < (SC_SSR_P_prob + SC_SSR_S_prob + SC_SR_P_prob + SC_SR_S_prob + SC_R_R_prob):
		return "[P] R"
	else:
		return "[S] R"
		
def gacha_SC_Last():
	global SC_SSR_P_prob, SC_SSR_S_prob, SC_SR_P_prob
	rand = random.randint(0,999)
	if rand < SC_SSR_P_prob:
		return "[P] SSR"
	elif rand < (SC_SSR_P_prob + SC_SSR_S_prob):
		return "[S] SSR"
	elif rand < (SC_SSR_P_prob + SC_SSR_S_prob + SC_SR_P_prob):
		return "[P] SR"
	else:
		return "[S] SR"
	
def multi_gacha_SC(number):
	sc_gacha_result = ""
	for i in range(number-1):
		sc_gacha_result += str(gacha_SC())
		sc_gacha_result += "\n"
	sc_gacha_result += str(gacha_SC_Last())
	return sc_gacha_result

def teach(user_message,teachmode):
	if teachmode == 0:
		reply_message = user_message.lstrip("!教育 ")
	elif teachmode == 1:
		reply_message = user_message.lstrip("!調教 ")
	split_result = reply_message.split(' ', 1 )
	if(len(split_result) <= 1):
		return "學習字詞失敗 > <"
	else:
		spreadsheet_key = "1RaGPlEJKQeg_xnUGi1mlUt95-Gc6n-XF_czwudIP5Qk"
		update_sheet_key(gss_client,spreadsheet_key,split_result[0],split_result[1])
		if teachmode == 0:
			success_learn ="已學習字詞 「"+split_result[0]+"」 !!!"
		elif teachmode == 1:
			success_learn ="我學會 「"+split_result[0]+"」 了 >////< "
		return success_learn

def leaderboard():
	list_top = []
	list_name = []
	list_score = []
	get_score_sheet(list_top,list_name,list_score,2)
	# print (list_top,list_name,list_score)
	score_str = ""
	for i in range(0,10):
		score_str += (str(list_top[i])+"\t"+list_name[i]+"\t"+list_score[i]+"\n")
	# print(score_str)
	return score_str

def your_pants():
	list_top = []
	list_name = []
	list_time = []
	get_score_sheet(list_top,list_name,list_time,6)
	# print (list_top,list_name,list_score)
	score_str = ""
	score_str += ("目前" + str(list_top[0])+"為\t"+list_name[0]+"\t\n")
	for i in range(1,10):
		score_str += (list_name[i]+"\t還需要 "+list_time[i]+" 才能脫 "+list_name[i-1]+" 的褲子\n")
	return score_str
	
def readme():
	with open('readme.txt', 'r') as f:
		content = f.read()
	return content
			
def slient_mode(user_message,event):
	global mode
	if(user_message == "!說話"):
		mode = 1 
		message = TextSendMessage(text='沒問題 ^_^，我來陪大家聊天惹，但如果覺得我太吵的話，請跟我說 「!閉嘴」 > <')
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message in ["!閉嘴","!安靜","!你閉嘴","!你安靜"]):
		mode = 0
		message = TextSendMessage(text='我已經閉嘴了 > <  (小聲)')
		line_bot_api.reply_message(event.reply_token,message)

def switch_on():
	global mode	
	mode = 1
	return '我已經正在說話囉，歡迎來跟我互動 ^_^ '

def switch_off():
	global mode	
	mode = 0
	return '好的，我乖乖閉嘴 > <，如果想要我繼續說話，請跟我說 「!說話」 > <'

def forget(user_message):
	reply_message = user_message.lstrip("!忘記 ")
	split_result = reply_message.split(' ', 1 )
	if(len(split_result) <= 1):
		return "忘記字詞失敗 > <"
	else:
		key = split_result[0]
		response = split_result[1]
	# Setup the Sheets API
	SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
	store = file.Storage('credentials.json')
	creds = store.get()
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
		creds = tools.run_flow(flow, store)
	service = build('sheets', 'v4', http=creds.authorize(Http()))

	# Call the Sheets API
	SPREADSHEET_ID = '1RaGPlEJKQeg_xnUGi1mlUt95-Gc6n-XF_czwudIP5Qk'
	RANGE_NAME = 'Sheet1!A2:B2000'
	result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
												 range=RANGE_NAME).execute()
	values = result.get('values', [])
	if not values:
		print('No data found.')
	else:
		list_key = []
		list_response = []
		for row in values:	
			list_key.append(row[0])
			list_response.append(row[1])
		print (len(list_key),len(list_response))	
		for i in range(0,len(list_key)):
			if(list_key[i]==key and list_response[i]==response):
				print (i)
				#clear_range = 'Sheet1!A'+str(i)+':B'+str(i)
				#sheet_request = service.spreadsheets().values().clear(spreadsheetId=SPREADSHEET_ID, range=clear_range).execute()
				wks = gss_client.open_by_key(SPREADSHEET_ID)
				sheet = wks.sheet1
				#sheet.delete_row(i)
				sheet.update_acell('A'+str(i), 'test')
				sheet.update_acell('B'+str(i), 'test')
				return "忘記字詞成功 !!!"
			else:
				return "忘記字詞失敗 > <"

CMD_Matrix = [ # exact cmd
[["!閉嘴","!安靜","!你閉嘴","!你安靜"],TextSendMessage(text = switch_off())],
[["!說話"],TextSendMessage(text = switch_on())],
[["即時排名","即時戰況"], TextSendMessage(text = leaderboard())],
[["!使用說明書","!help"], TextSendMessage(text = readme())],
[["脫褲子","脫內褲"], TextSendMessage(text = your_pants())],
[["貼圖辣","貼圖啦","貼圖","貼圖喇"], StickerSendMessage(package_id='2',sticker_id = str(random.randint(140,180)))],
[["母湯"], VideoSendMessage(
	original_content_url = 'https://i.imgur.com/Upmorh0.mp4',
	preview_image_url = 'https://i.imgur.com/Upmorh0.gif'
	)],
[["母湯電影版"], ImageSendMessage(
		original_content_url = "https://i.imgur.com/rUZ4AdD.jpg",
		preview_image_url = "https://i.imgur.com/rUZ4AdD.jpg"
	)],
[["!抽食物"], TextSendMessage(text = get_food_sheet(1))],
[["!抽飲料"], TextSendMessage(text = get_food_sheet(2))],
[["!cgss單抽"]
	, TextSendMessage(text ="【您抽到的是：】\n" + gacha_CGSS())],
[["!cgss十連","!cgss十抽","!cgss10連","!cgss10抽"]
	, TextSendMessage(text ="【您抽到的是：】\n" + ten_gacha_CGSS())],
[["!bgd單抽","!gbp單抽"]
	, TextSendMessage(text = "【您抽到的是：】\n" + gacha_BGD())],
[["!bgd十連","!bgd十抽","!bgd10連","!bgd10抽","!gbp十連","!gbp十抽","!gbp10連","!gbp10抽"]
	, TextSendMessage(text = "【您抽到的是：】\n" + ten_gacha_BGD())],
[["!sc單抽"]
	, TextSendMessage(text ="【SC 單抽結果】\n" + multi_gacha_SC(1))],
[["!sc十連","!sc十抽","!sc10連","!sc10抽"]
	, TextSendMessage(text ="【SC 10連結果】\n" + multi_gacha_SC(10))]
]

CMD_Matrix_2 = [] # find functions add later

def active_mode(user_message,event):
	'''global CMD_Matrix
	for i in range(len(CMD_Matrix)):
		if(user_message.lower() in CMD_Matrix[i][0]):
			message = CMD_Matrix[i][1]
			print(mode)
			line_bot_api.reply_message(event.reply_token,message)
			# don't execute the following commands if Matrix 1 is executed.'''
	global mode
	if(user_message in ["!閉嘴","!安靜","!你閉嘴","!你安靜"]):
		mode = 0
		message = TextSendMessage(text='好的，我乖乖閉嘴 > <，如果想要我繼續說話，請跟我說 「!說話」 > <')
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message == "!說話"):
		mode = 1
		message = TextSendMessage(text='我已經正在說話囉，歡迎來跟我互動 ^_^ ')
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message == "!使用說明書"):
		readme_text = readme()
		message = TextSendMessage(text=readme_text)
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message in CMD_Matrix[0][0]):
		message = CMD_Matrix[0][1]
		line_bot_api.reply_message(event.reply_token,message)
		# line_bot_api.push_message(user_id,TextSendMessage(text=score_str))
	elif(user_message in ["脫褲子","脫內褲"]):
		score_str = your_pants()
		message = TextSendMessage(text=score_str)
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message in ["貼圖辣","貼圖啦","貼圖","貼圖喇"]):
		randsticker = random.randint(140,180)
		message = StickerSendMessage(package_id='2',sticker_id=str(randsticker = random.randint(140,180)))
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message == "母湯電影版"):		
		message = VideoSendMessage(
		original_content_url='https://i.imgur.com/Upmorh0.mp4',
		preview_image_url='https://i.imgur.com/Upmorh0.gif'
		)
		line_bot_api.reply_message(event.reply_token, message)
	elif(user_message == "!抽食物"):
		food = get_food_sheet(1)
		message = TextSendMessage(text=food)
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message == "!抽飲料"):
		food = get_food_sheet(2)
		message = TextSendMessage(text=food)
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message == "!CGSS單抽"):
		result = "【您抽到的是：】\n"
		result += gacha_CGSS()
		message = TextSendMessage(text=result)
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message in ["!CGSS十連","!CGSS十抽","!CGSS10連","!CGSS10抽"]):
		result = "【您抽到的是：】\n"
		result += ten_gacha_CGSS()
		message = TextSendMessage(text=result)
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message in ["!BGD單抽","!bgd單抽"]):
		result = "【您抽到的是：】\n"
		result += gacha_BGD()
		message = TextSendMessage(text=result)
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message in ["!BGD十連","!BGD十抽","!BGD10連","!BGD10抽","!bgd十連","!bgd十抽","!bgd10連","!bgd10抽"]):
		result = "【您抽到的是：】\n"
		result += ten_gacha_BGD()
		message = TextSendMessage(text=result)
		line_bot_api.reply_message(event.reply_token,message)

	# ------ below are find function ------	 
	if(user_message.find("母湯") >= 0):
		message = ImageSendMessage(
			original_content_url= "https://i.imgur.com/rUZ4AdD.jpg",
			preview_image_url= "https://i.imgur.com/rUZ4AdD.jpg"
		)
		line_bot_api.reply_message(event.reply_token, message)
	elif(user_message.find("!機率") == 0):
		probability = random.randint(0,101)
		reply_message = user_message.lstrip("!機率 ")
		reply_message = "嗯... 我覺得 "+reply_message + " 的機率是 "+ str(probability) + " % !!!"
		message = TextSendMessage(text=reply_message)
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message.find("!抽數字") == 0):
		reply_message = user_message.lstrip("!抽數字 ")
		random_number = random.randint(1,int(reply_message))
		message = TextSendMessage(text=random_number)
		line_bot_api.reply_message(event.reply_token,message)		
	elif(user_message.find("!教育") == 0):
		teach_result = teach(user_message,0)
		message = TextSendMessage(text=teach_result)
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message.find("!調教") == 0):
		teach_result = teach(user_message,1)
		message = TextSendMessage(text=teach_result)
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message.find("!忘記") == 0):
		forget_result = forget(user_message)
		message = TextSendMessage(text=forget_result)
		line_bot_api.reply_message(event.reply_token,message)
	else:
		key_message = get_key_response(user_message)
		if key_message != 0:
			message = TextSendMessage(text=key_message)
			line_bot_api.reply_message(event.reply_token,message)
	#for i in range
	
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
	global mode 
	print("now: "+str(today))
	print("mode: "+str(mode))
	print(event)		
	user_message = event.message.text
	
	if(user_message== "test"):
		message = TextSendMessage(text='Hello World !!!')
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message== "state"):
		message = TextSendMessage(
			text="(silent mode)" if mode == 0 else "(active mode)"
		)
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message== "!重新開機" or user_message == "!restart"):
		message = TextSendMessage(text="restarting...")
		line_bot_api.reply_message(event.reply_token,message)
		sys.exit(0)
	elif(mode == 0):
		slient_mode(user_message,event) 
	elif(mode == 1):
		active_mode(user_message,event)
		
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
	
# notes 
	
#push message to one user
# line_bot_api.push_message(user_id, 
    # TextSendMessage(text='Hello World!'))
# push message to multiple users
# line_bot_api.multicast(['user_id1', 'user_id2'], 
    # TextSendMessage(text='Hello World!'))	

# lineuserid = event.source.userId
# messageid = event.message.id
# lineuserid = "howard"
# messagetype = event.message.type
# text = event.message.text
# message = TextSendMessage(text)

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
		