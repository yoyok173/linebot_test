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

app = Flask(__name__)
# Channel Access Token
line_bot_api = LineBotApi('+wjG+A6ltvlFVrmQmxyBaXcfljMtYaCTMXnVBoTxhWwMcSRX9+1mMObUO6oVongrp2y7parq1a1/bbbwvOhn/iO26lASkwoWX1u0HBisf7ZRr4cfMzcXFYM/8eFwpeQkdcXYz2obPYl1sE6+kWyC4QdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('4c154ea12f7a284b5edd99087d760143')
# user_id = "Udf8f28a8b752786fa7a6be7d8c808ec6"
auth_json_path = "./auth.json"

now = datetime.datetime.now()
mode = 1

# game SSR Prob
SC_SSR_P_prob = 20 # SC Produce idol SSR_probability
SC_SSR_S_prob = 30 # SC Support idol SSR_probability
SC_SR_P_prob = 60 # SC Produce idol SR_probability
SC_SR_S_prob = 100 # SC Support idol SR_probability
SC_R_R_prob = 290 # SC Support idol R_probability

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

score_sheet_ID = '1F0aMMBcADRSXm07IT2Bxb_h22cIjNXlsCfBYRk53PHA'
my_database_sheet_ID = '1RaGPlEJKQeg_xnUGi1mlUt95-Gc6n-XF_czwudIP5Qk'
april_ID='Udf8f28a8b752786fa7a6be7d8c808ec6'


def get_value_from_google_sheet(SPREADSHEET_ID,RANGE_NAME):
	# Setup the Sheets API
	SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
	store = file.Storage('credentials.json')
	creds = store.get()
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
		creds = tools.run_flow(flow, store)
	service = build('sheets', 'v4', http=creds.authorize(Http()))

	# Call the Sheets API
	result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
												 range=RANGE_NAME).execute()
	return result.get('values', [])

values = get_value_from_google_sheet(my_database_sheet_ID,'dictionary!A2:C1000')

list_key = []
list_response = []
list_type = []
for row in values:	
	list_key.append(row[0])
	list_response.append(row[1])
	list_type.append(row[2])

def get_score_sheet(list_top,list_name,list_target,target):
	global score_sheet_ID
	values = get_value_from_google_sheet(score_sheet_ID,'A2:M11')
	if not values:
		print('No data found.')
	else:
		for row in values:	
			list_top.append(row[0])
			list_name.append(row[1])
			list_target.append(row[target])
		
def get_key_response(key):
	global list_key
	global list_response
	global list_type
	if key in list_key:
		# list_response = list_key.index(key)
		list_response_index = [i for i,v in enumerate(list_key) if v==key]
		print (list_response_index)
		random_reply = random.randint(0,len(list_response_index)-1)
		response_index = list_response_index[random_reply]
		if(list_type[response_index]=="str"):
			message = TextSendMessage(text=list_response[response_index])
		elif(list_type[response_index]=="pic"):
			content = list_response[response_index]
			message = ImageSendMessage(
			original_content_url= content,
			preview_image_url= content
			)
		return message
	else:
		return 0
		
def auth_gss_client(path, scopes):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(path,scopes)
    return gspread.authorize(credentials)

gss_scopes = ['https://spreadsheets.google.com/feeds']
gss_client = auth_gss_client(auth_json_path, gss_scopes)

def update_sheet_key(gss_client, key, input , output):
	global list_key,list_response,list_type
	try:
		wks = gss_client.open_by_key(key)
		sheet = wks.worksheet('dictionary')
		sheet.insert_row([input , output,"str"], 2)
		list_key.append(input)
		list_response.append(output)
		list_type.append("str")
		return "success"
	except:
		line_bot_api.push_message(april_ID, TextSendMessage(text='智乃壞掉囉~~~'))
		return "看來是google又壞掉了QQ，我已經幫忙通知拔拔了! 請稍等~~"

def update_pic_sheet_key(gss_client, key, input , output):
	global list_key,list_response,list_type
	try:
		wks = gss_client.open_by_key(key)
		sheet = wks.worksheet('dictionary')
		sheet.insert_row([input , output,"pic"], 2)
		list_key.append(input)
		list_response.append(output)
		list_type.append("pic")
		return "success"
	except:
		line_bot_api.push_message(april_ID, TextSendMessage(text='智乃壞掉囉~~~'))
		return "看來是google又壞掉了QQ，我已經幫忙通知拔拔了! 請稍等~~"

def get_food_sheet(key):
	global my_database_sheet_ID
	if key == 1:
		values = get_value_from_google_sheet(my_database_sheet_ID,'food!A2:A')
	elif key == 2:
		values = get_value_from_google_sheet(my_database_sheet_ID,'food!B2:B')
	if not values:
		print('No data found.')
	else:
		list_food = []
		for row in values:	
			list_food.append(row[0])
			
		random_food_index = random.randint(0,len(list_food)-1)
		return str(list_food[random_food_index])

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
	global my_database_sheet_ID
	try:
		split_result = user_message.split(' ', 2 )
	except:
		return "【請依照範例輸入：】\n!教育 (關鍵字) (網址)\n!調教 (關鍵字) (網址)"
	else:
		message = update_sheet_key(gss_client,my_database_sheet_ID,split_result[1],split_result[2])
		if message == "success":
			if teachmode == 0:
				return "我學會了 「"+split_result[0]+"」 !"
			elif teachmode == 1:
				return "學會 「"+split_result[0]+"」 了 >////< "
		else:
			return message 

def teach_pic(user_message,key):
	global my_database_sheet_ID	
	try:
		split_result = user_message.split(' ', 2 )
	except:
		return "【請依照範例輸入：】\n!給智乃看圖 (關鍵字) (網址)\n!智乃看圖片 (關鍵字) (網址)\n!智乃看圖圖 (關鍵字) (網址)"
	else:
		message = update_pic_sheet_key(gss_client,my_database_sheet_ID,split_result[1],split_result[2])
		if message == "success":
			if key == 0:
				return "哇嗚~ 好好看的「"+split_result[0]+"」 圖 >////< "
			elif key == 1:
				return "哇嗚~ 這「"+split_result[0]+"」 圖 >////< "
			elif key == 2:
				return "「"+split_result[0]+"」 圖圖怎麼這麼好看 >////< "
		else:
			return message

def leaderboard(key):
	list_top = []
	list_name = []
	list_score = []
	get_score_sheet(list_top,list_name,list_score,key)
	# print (list_top,list_name,list_score)
	score_str = ""
	for i in range(0,10):
		score_str += (str(list_top[i])+" --- "+list_score[i]+"\n【"+list_name[i]+"】\n")
	# print(score_str)
	score_str += str((datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y/%m/%d %H:%M:%S"))
	# score_str += str(time.strftime("%c"))
	return score_str

def event_progress():
	global score_sheet_ID
	values = get_value_from_google_sheet(score_sheet_ID,'E15')
	if not values:
		print('No data found.')
	else:
		for row in values:	
			return row[0]

def event_remain_time():
	global score_sheet_ID
	values = get_value_from_google_sheet(score_sheet_ID,'E17')
	if not values:
		print('No data found.')
	else:
		for row in values:	
			return row[0]
	
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
	elif(user_message == "!閉嘴"):
		mode = 0
		message = TextSendMessage(text='我已經閉嘴了 > <  (小聲)')
		line_bot_api.reply_message(event.reply_token,message)

def switch_still_on():
	global mode	
	mode = 1
	return '我已經正在說話囉，歡迎來跟我互動 ^_^ '

def switch_off():
	global mode	
	mode = 0
	return '好的，我乖乖閉嘴 > <，如果想要我繼續說話，請跟我說 「!說話」 > <'

def room_get():
	global my_database_sheet_ID
	list_room = []
	values = get_value_from_google_sheet(my_database_sheet_ID,'room!A1:A')
	if not values:
		print('No data found.')
	else:
		for row in values:	
			list_room.append(row[0])
		return "當前房號1為： "+list_room[0]+"\n當前房號2為： "+list_room[1]

def room_update(user_message):
	global my_database_sheet_ID
	try:
		room_number = user_message.split(" ",1)
		print("get new number : "+room_number[1])
	except:
		return "請依照範例輸入：【room1 12345】"

	try:
		wks = gss_client.open_by_key(my_database_sheet_ID)
		sheet = wks.worksheet('room')
		sheet.update_acell('A1', room_number[1])
		return "當前房號1已更新為："+room_number[1]	
	except:
		line_bot_api.push_message(april_ID, TextSendMessage(text='智乃壞掉囉~~~'))
		return "看來是google又壞掉了QQ，我已經幫忙通知四月拔拔了! 請稍等~~"

def room_update2(user_message):
	global my_database_sheet_ID
	try:
		room_number = user_message.split(" ",1)
		print("get new number : "+room_number[1])
	except:
		return "請依照範例輸入：【room2 12345】"

	try:
		wks = gss_client.open_by_key(my_database_sheet_ID)
		sheet = wks.worksheet('room')
		sheet.update_acell('A2', room_number[1])
		return "當前房號1已更新為："+room_number[1]	
	except:
		line_bot_api.push_message(april_ID, TextSendMessage(text='智乃壞掉囉~~~'))
		return "看來是google又壞掉了QQ，我已經幫忙通知四月拔拔了! 請稍等~~"

'''
def forget(user_message):
	global dictionary_sheet
	reply_message = user_message.lstrip("!忘記 ")
	split_result = reply_message.split(' ',1)
	print(split_result)
	if(len(split_result) <= 1):
		return "忘記字詞失敗 > < 你好歹也告訴我要忘記的內容是什麼吧?"
	elif(split_result[0]=="智乃"):
		return "oh~ 抱歉~ 我學過的東西是不會忘記的 =) "
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
	RANGE_NAME = 'Sheet1!A2:B1000'
	dictionary_sheet = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
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
		if key in list_key:	
			for i in range(0,len(list_key)):
				if(list_key[i]==key and list_response[i]==response):
					print (i)
					wks = gss_client.open_by_key(SPREADSHEET_ID)
					sheet = wks.sheet1
					#sheet.delete_row(i)
					sheet.update_acell('A'+str(i+2), 'test')
					sheet.update_acell('B'+str(i+2), 'test')
					return "忘記字詞 「"+key+"」 成功 !!!"
			return "忘記字詞失敗 > < 你是不是連自己教過的東西都忘了?"
		else:
			return "忘記字詞失敗 > < 你確定有教過我這個詞?"
'''

'''
def search_cmd(user_message):
	operations_str = [
	[["!閉嘴","!安靜","!你閉嘴","!你安靜"],switch_off()],
	[["!說話"],switch_still_on()],
	[["!使用說明書","!help","!說明書"],readme()],
	[["即時排名","即時戰況",'排名','分數','戰況','score'],leaderboard(2)],
	[["%數","%"],leaderboard(3)],
	[['分數差'],leaderboard(5)],
	[['場數差'],leaderboard(6)], 
	[["追擊時間","脫褲子","脫內褲","內褲","褲子"],leaderboard(7)],
	[['時速'],leaderboard(8)], 
	[['場速'],leaderboard(9)],
	[["活動進度",'進度'],event_progress()],
	[["!抽食物","!食物",'!food'],get_food_sheet(1)],
	[["!抽飲料","!飲料",'!drink'],get_food_sheet(2)],
	[["!cgss單抽"],"【CGSS 單抽結果】\n" + gacha_CGSS()],
	[["!cgss十連","!cgss十抽","!cgss10連","!cgss10抽"],"【CGSS 10連結果】\n" + ten_gacha_CGSS()],
	[["!bgd單抽","!gbp單抽"],"【BGD 單抽結果】\n" + gacha_BGD()],
	[["!bgd十連","!bgd十抽","!bgd10連","!bgd10抽","!gbp十連","!gbp十抽","!gbp10連","!gbp10抽"],"【BGD 10連結果】\n" + ten_gacha_BGD()],
	[["!sc單抽"],"【SC 單抽結果】\n" + multi_gacha_SC(1)],
	[["!sc十連","!sc十抽","!sc10連","!sc10抽"],"【SC 10連結果】\n" + multi_gacha_SC(10)]
	]

	print(len(operations_str))
	for i in range(len(operations_str)):
		if user_message in operations_str[i][0]:
			return TextSendMessage(text= operations_str[i][1])
	print("key not found in cmd box !")
	return "not found in cmd list"
'''

def other_type_message(user_message):
	if(user_message in ["貼圖辣","貼圖啦","貼圖","貼圖喇"]):
		message = StickerSendMessage(package_id='2',sticker_id=str(random.randint(140,180)))
	elif(user_message == "母湯電影版"):		
		message = VideoSendMessage(
		original_content_url='https://i.imgur.com/Upmorh0.mp4',
		preview_image_url='https://i.imgur.com/Upmorh0.gif'
		)
	# ------ below are find function ------	 
	elif(user_message.find("母湯") >= 0):
		message = ImageSendMessage(
			original_content_url= "https://i.imgur.com/rUZ4AdD.jpg",
			preview_image_url= "https://i.imgur.com/rUZ4AdD.jpg"
		)
	elif(user_message == "!開關"):
		# random_result = random.randint(0,1)
		# answer = ["幹你娘","恭喜你獲得了空虛！"]
		message = TemplateSendMessage(
			alt_text='【請問您今天要來點靜音嗎？】',
			template=ConfirmTemplate(
				text='【請問您今天要來點靜音嗎？】',
				actions=[
				PostbackTemplateAction(
					label='請靜音',
					text='!閉嘴',
					data='action=buy&itemid=1'
					),
				MessageTemplateAction(
					label='繼續說話',
					text='!說話'
					)
				]
			)
		)
	elif(user_message == "機會命運"):
		# random_result = random.randint(0,1)
		# answer = ["幹你娘","恭喜你獲得了空虛！"]
		message = TemplateSendMessage(
			alt_text='【機會命運】',
			template=ConfirmTemplate(
				text='【四月、智乃請選擇？】',
				actions=[
				PostbackTemplateAction(
					label='四月',
					text='四月',
					data='action=buy&itemid=1'
					),
				MessageTemplateAction(
					label='智乃',
					text='智乃'
					)
				]
			)
		)
	elif(user_message == "好餓"):
		# random_result = random.randint(0,1)
		# answer = ["幹你娘","恭喜你獲得了空虛！"]
		message = TemplateSendMessage(
			alt_text='【好餓好餓】',
			template=ConfirmTemplate(
				text='【食物、飲料請選擇？】',
				actions=[
				PostbackTemplateAction(
					label='食物',
					text='!抽食物',
					data='action=buy&itemid=1'
					),
				MessageTemplateAction(
					label='飲料',
					text='!抽飲料'
					)
				]
			)
		)
	elif(user_message == "!抽抽"):
		message = TemplateSendMessage(
			alt_text='【請問你要哪一個抽抽池呢？】',
			template=CarouselTemplate(
				columns=[
					CarouselColumn(
						thumbnail_image_url='https://i.imgur.com/jaLz5Hk.jpg',
						title='ガルパ',
						text='BanK Dream! Girls Bank Party!',
						actions=[
							PostbackTemplateAction(
								label='1回ガチャ',
								text='!BGD單抽',
								data='action=buy&itemid=1'
							),
							MessageTemplateAction(
								label='10回ガチャ',
								text='!BGD10連'
							),
							# URITemplateAction(
							# 	label='uri1',
							# 	uri='http://example.com/1'
							# )
						]
					),
					CarouselColumn(
						thumbnail_image_url='https://i.imgur.com/qpL7l3s.png',
						title='デレステ',
						text='我什麼都沒有Q_Q',
						actions=[
							PostbackTemplateAction(
								label='1回ガチャ',
								text='!CGSS單抽',
								data='action=buy&itemid=2'
							),
							MessageTemplateAction(
								label='10回ガチャ',
								text='!CGSS10連'
							),
							# URITemplateAction(
							# label='uri2',
							# uri='http://example.com/2'
							# )
						]
					)
				]
			)
		)
	else:
		print ("start finding library")
		message = get_key_response(user_message)

	if message != 0:
		return message
	else:
		return 0

def text_message(user_message):
	message = "default"
	if(user_message in ["!閉嘴"]):
		message = switch_off()
	elif(user_message in ["!說話"]):
		message = switch_still_on()
	elif(user_message in ["!使用說明書","!help","!說明書"]):
		message = readme()
	elif(user_message in ["即時排名","即時戰況",'排名','分數','戰況','score']):
		message = leaderboard(2)
	elif(user_message in ["%數","%"]):
		message = leaderboard(3)
	elif(user_message in ['一位差']):
		message = leaderboard(4)
	elif(user_message in ['分數差']):
		message = leaderboard(5)
	elif(user_message in ['場數差']):
		message = leaderboard(6)
	elif(user_message in ["追擊時間","脫褲子"]):
		message = leaderboard(7)
	elif(user_message in ['時速']):
		message = leaderboard(8)
	elif(user_message in ['場速']):
		message = leaderboard(9)
	elif(user_message in ["活動進度",'進度']):
		message = event_progress()
	elif(user_message in ["剩餘時間"]):
		message = event_remain_time()
	elif(user_message in ["房號","room"]):
		message = room_get()
	elif(user_message.find("room1") == 0):
		message = room_update(user_message)
	elif(user_message.find("room2") == 0):
		message = room_update2(user_message)
	elif(user_message.lower()  in ["!抽食物"]):
		message = get_food_sheet(1)
	elif(user_message.lower()  in ["!抽飲料"]):
		message = get_food_sheet(2)
	elif(user_message in ["!CGSS單抽"]):
		message = "【CGSS 單抽結果】\n" + gacha_CGSS()
	elif(user_message in ["!CGSS10連"]):
		message = "【CGSS 10連結果】\n" + ten_gacha_CGSS()
	elif(user_message in ["!BGD單抽"]):
		message = "【BGD 單抽結果】\n" + gacha_BGD()
	elif(user_message in ["!BGD10連"]):
		message = "【BGD 10連結果】\n" + ten_gacha_BGD()
	elif(user_message.lower()  in ["!sc單抽"]):
		message = "【SC 單抽結果】\n" + multi_gacha_SC(1)
	elif(user_message.lower()  in ["!sc十連","!sc十抽","!sc10連","!sc10抽"]):
		message = "【SC 10連結果】\n" + multi_gacha_SC(10)
	# ------ below are find function ------	 
	elif(user_message.find("!機率") == 0):
		try:
			reply_message = user_message.split(" ",1)
			message = "嗯... 我覺得 "+reply_message[1] + " 的機率是 "+ str(random.randint(0,101)) + " % !!!"
		except:
			message = "【請依照範例輸入：】\n!機率 (想預測的事情)"
	elif(user_message.find("!抽數字") == 0):
		try:
			reply_message = user_message.split(" ",1)		
			message = random.randint(1,int(reply_message[1]))
		except:
			message = "【請依照範例輸入：】\n!抽數字 (你的數字)\n(「1~你的數字」抽一個數字)"
	elif(user_message.find("!教育") == 0):
		message = teach(user_message,0)
	elif(user_message.find("!調教") == 0):
		message = teach(user_message,1)
	elif(user_message.find("!智乃看圖片") == 0):
		message = teach_pic(user_message,0)
	elif(user_message.find("!給智乃看圖") == 0):
		message = teach_pic(user_message,1)
	elif(user_message.find("!智乃看圖圖") == 0):
		message = teach_pic(user_message,2)
	# elif(user_message.find("!忘記") == 0):
	# 	forget_result = forget(user_message)
	# 	message = TextSendMessage(text=forget_result)
	# 	line_bot_api.reply_message(event.reply_token,message)

	if message != "default" :
		return TextSendMessage(text=message)
	else:
		return other_type_message(user_message)

def active_mode(user_message,event):
	'''
	print("start atcive mode key word serach...")
	global mode
	message_get = search_cmd(user_message.lower())
	if str(message_get) != "not found in cmd list" :
		line_bot_api.reply_message(event.reply_token,message_get)
	'''
	message = text_message(user_message)
	print(message)
	if message != 0:
		line_bot_api.reply_message(event.reply_token,message)
	
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
	print("now: "+str((datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y/%m/%d %H:%M:%S")))
	print("mode: "+str(mode))
	print("event: " +str(event))		
	user_message = event.message.text
	
	if(user_message== "test"):
		message = TextSendMessage(text='Hello World !!!')
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message== "state"):
		message = TextSendMessage(
			text="(silent mode)" if mode == 0 else "(active mode)"
		)
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message in ["!getinfo"]):
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text=str(event)))
	elif(user_message in ["!壞掉啦","呼叫工程師","呼叫四月"]):
		line_bot_api.push_message(april_ID, TextSendMessage(text='智乃壞掉囉~~~'))
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已經幫您通知四月拔拔了! 請稍等~~"))
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