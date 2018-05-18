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