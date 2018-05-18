
import gspread
import json

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from urllib.request import urlopen
from oauth2client.service_account import ServiceAccountCredentials

my_database_sheet_ID = '1RaGPlEJKQeg_xnUGi1mlUt95-Gc6n-XF_czwudIP5Qk'
auth_json_path = "./auth.json"

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
'''		
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
'''


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