
import gspread
import datetime

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from urllib.request import urlopen
from oauth2client.service_account import ServiceAccountCredentials

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
	MessageEvent, TextMessage, TextSendMessage,
)

# Channel Access Token
line_bot_api = LineBotApi('+wjG+A6ltvlFVrmQmxyBaXcfljMtYaCTMXnVBoTxhWwMcSRX9+1mMObUO6oVongrp2y7parq1a1/bbbwvOhn/iO26lASkwoWX1u0HBisf7ZRr4cfMzcXFYM/8eFwpeQkdcXYz2obPYl1sE6+kWyC4QdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('4c154ea12f7a284b5edd99087d760143')

score_sheet_ID = '1F0aMMBcADRSXm07IT2Bxb_h22cIjNXlsCfBYRk53PHA'
my_database_sheet_ID = '1RaGPlEJKQeg_xnUGi1mlUt95-Gc6n-XF_czwudIP5Qk'
april_ID='Udf8f28a8b752786fa7a6be7d8c808ec6'
auth_json_path = "./auth.json"

def auth_gss_client(path, scopes):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(path,scopes)
    return gspread.authorize(credentials)

gss_scopes = ['https://spreadsheets.google.com/feeds']
gss_client = auth_gss_client(auth_json_path, gss_scopes)

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

def event_board(key):
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
		return "【請依照範例輸入：】\nroom1 12345"

	# try:
	wks = gss_client.open_by_key(my_database_sheet_ID)
	sheet = wks.worksheet('room')
	sheet.update_acell('A1', room_number[1])
	return "當前房號1已更新為："+room_number[1]	
	# except:
	# 	line_bot_api.push_message(april_ID, TextSendMessage(text='智乃壞掉囉~~~'))
	# 	return "看來是google又壞掉了QQ，我已經幫忙通知四月拔拔了! 請稍等~~"

def room_update2(user_message):
	global my_database_sheet_ID
	try:
		room_number = user_message.split(" ",1)
		print("get new number : "+room_number[1])
	except:
		return "【請依照範例輸入：】\nroom2 12345"

	# try:
	wks = gss_client.open_by_key(my_database_sheet_ID)
	sheet = wks.worksheet('room')
	sheet.update_acell('A2', room_number[1])
	return "當前房號2已更新為："+room_number[1]	
	# except:
	# 	line_bot_api.push_message(april_ID, TextSendMessage(text='智乃壞掉囉~~~'))
	# 	return "看來是google又壞掉了QQ，我已經幫忙通知四月拔拔了! 請稍等~~"

def fire_calculator(user_message):
	try:
		split = user_message.split(" ",1)
		if(split=="?"):
			return "【請依照範例輸入：】\n!fire (剩餘火量) (活動％數不用打％)"
		else:
			fire = split[1]
	except:
		return "【請依照範例輸入：】\n!fire (剩餘火量) (活動％數,不用打％)"

	message = "目前所剩石頭量:"+str(fire)+"\n可轉換分數:"+str(int(fire/3*(1+((score)/100))))
	return message

def stone_calculator(user_message):
	global score_sheet_ID
	try:
		split = user_message.split(" ",2)
		stone = split[1]
		score = split[2]
	except:
		return "【請依照範例輸入：】\n!stone (剩餘石頭) (活動％數,不用打％)"

	values = get_value_from_google_sheet(score_sheet_ID,'E14')
	if not values:
		print('No data found.')
	else:
		for row in values:	
			time = 120-row[0]
	message = "活動剩餘時間:"+str(time)+"\n目前所剩石頭量:"+str(stone)+"\n全速到結束所需石頭:"+str(int(time*25*3*100/10))+"\n仍缺少石頭:"+str(int(time*25*3*100/10)-stone)+"\n剩餘石頭可轉換分數:"+str(int(stone/100*10/3*(1+((score)/100)))
	return message

