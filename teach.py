
import gspread
import json

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from urllib.request import urlopen
from oauth2client.service_account import ServiceAccountCredentials

my_database_sheet_ID = '1RaGPlEJKQeg_xnUGi1mlUt95-Gc6n-XF_czwudIP5Qk'


def auth_gss_client(path, scopes):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(path,scopes)
    return gspread.authorize(credentials)

gss_scopes = ['https://spreadsheets.google.com/feeds']
gss_client = auth_gss_client(auth_json_path, gss_scopes)


def update_sheet_key(gss_client, key, input , output):
	global list_key,list_response,list_type
	# try:
	wks = gss_client.open_by_key(key)
	sheet = wks.worksheet('dictionary')
	sheet.insert_row([input , output,"str"], 2)
	list_key.append(input)
	list_response.append(output)
	list_type.append("str")
	return "success"
	# except:
	# 	line_bot_api.push_message(april_ID, TextSendMessage(text='智乃壞掉囉~~~'))
	# 	return "看來是google又壞掉了QQ，我已經幫忙通知拔拔了! 請稍等~~"

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


def teach(user_message,teachmode):
	global my_database_sheet_ID
	# try:
	split_result = user_message.split(' ', 2 )
	print(split_result)
	message = update_sheet_key(gss_client,my_database_sheet_ID,split_result[1],split_result[2])
	if message == "success":
		if teachmode == 0:
			return "我學會了 「"+split_result[1]+"」 !!!"
		elif teachmode == 1:
			return "學會 「"+split_result[1]+"」 了 >////< "
	else:
		return message 
	# except:
	# 	return "【請依照範例輸入：】\n!教育 (關鍵字) (反應)\n!調教 (關鍵字) (反應)"
	
def teach_pic(user_message,key):
	global my_database_sheet_ID	
	try:
		split_result = user_message.split(' ', 2 )
		print(split_result)
		message = update_pic_sheet_key(gss_client,my_database_sheet_ID,split_result[1],split_result[2])
		if message == "success":
			if key == 0:
				return "哇嗚~ 好好看的「"+split_result[1]+"」 圖 >////< "
			elif key == 1:
				return "哇嗚~ 這「"+split_result[1]+"」 圖 >////< "
			elif key == 2:
				return "「"+split_result[1]+"」 圖圖怎麼這麼好看 >////< "
		else:
			return message
	except:
		return "【請依照範例輸入：】\n!給智乃看圖 (關鍵字) (網址)\n!智乃看圖片 (關鍵字) (網址)\n!智乃看圖圖 (關鍵字) (網址)"