
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
import gacha as gacha
import game_set as game
import event as event
import teach as teach
import slient_mode as slient
import switch as switch
import food as food 
import notebook as note

# Channel Access Token
line_bot_api = LineBotApi('+wjG+A6ltvlFVrmQmxyBaXcfljMtYaCTMXnVBoTxhWwMcSRX9+1mMObUO6oVongrp2y7parq1a1/bbbwvOhn/iO26lASkwoWX1u0HBisf7ZRr4cfMzcXFYM/8eFwpeQkdcXYz2obPYl1sE6+kWyC4QdB04t89/1O/w1cDnyilFU=')


def other_type_message(user_message):
	if(user_message in ["貼圖辣","貼圖啦","貼圖","貼圖喇"]):
		message = StickerSendMessage(package_id='2',sticker_id=str(random.randint(140,180)))
	elif(user_message == "母湯電影版"):		
		message = VideoSendMessage(
		original_content_url='https://i.imgur.com/Upmorh0.mp4',
		preview_image_url='https://i.imgur.com/Upmorh0.gif'
		) 
	elif(user_message.find("母湯") >= 0):
		message = ImageSendMessage(
			original_content_url= "https://i.imgur.com/rUZ4AdD.jpg",
			preview_image_url= "https://i.imgur.com/rUZ4AdD.jpg"
		)
	elif(user_message == "!開關"):
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
		random_result = random.randint(0,1)
		answer = ["ＱＱ，你死惹","恭喜！你活下來了！"]
		message = TemplateSendMessage(
			alt_text='【機會命運】',
			template=ConfirmTemplate(
				text='【機會、命運請選擇？】\n(一個會死、一個會活下來)',
				actions=[
				PostbackTemplateAction(
					label='機會',
					text= answer[random_result],
					data='action=buy&itemid=1'
					),
				MessageTemplateAction(
					label='命運',
					text= answer[1-random_result]
					)
				]
			)
		)
	elif(user_message == "好餓"):
		message = TemplateSendMessage(
			alt_text='【要吃食物、還是喝飲料呢？】',
			template=CarouselTemplate(
				columns=[
					CarouselColumn(
						thumbnail_image_url='https://i.imgur.com/yrY5mkt.jpg',
						title='【今天要吃什麼呢～？】',
						text='【今天要吃什麼呢～？】',
						actions=[
							PostbackTemplateAction(
								label='抽食物',
								text='!抽食物',
								data='action=buy&itemid=1'
							),
							MessageTemplateAction(
								label='抽食物',
								text='!抽食物'
							),
							# URITemplateAction(
							# 	label='uri1',
							# 	uri='http://example.com/1'
							# )
						]
					),
					CarouselColumn(
						thumbnail_image_url='https://i.imgur.com/YAyNSub.jpg',
						title='【今天要喝什麼呢～？】',
						text='【今天要喝什麼呢～？】',
						actions=[
							PostbackTemplateAction(
								label='抽飲料',
								text='!抽飲料',
								data='action=buy&itemid=1'
							),
							MessageTemplateAction(
								label='抽飲料',
								text='!抽飲料'
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
	elif(user_message == "小遊戲"):
		message = TemplateSendMessage(
			alt_text='【請問您要哪一種小遊戲呢？】',
			template=CarouselTemplate(
				columns=[
					CarouselColumn(
						thumbnail_image_url='https://i.imgur.com/02b6MnB.jpg',
						title='終極密碼',
						text='猜數字1~99，比誰反應的快',
						actions=[
							PostbackTemplateAction(
								label='終極密碼',
								text='!終極密碼',
								data='action=buy&itemid=1'
							),
							MessageTemplateAction(
								label='終極密碼',
								text='!終極密碼'
							),
							# URITemplateAction(
							# 	label='uri1',
							# 	uri='http://example.com/1'
							# )
						]
					),
					CarouselColumn(
						thumbnail_image_url='https://i.imgur.com/02b6MnB.jpg',
						title='幾Ａ幾Ｂ',
						text='猜一個四位不重複的數字，A表示數字對位置對，B表示數字錯位置錯，透過已知的線索，來看看你能多快猜到數字吧！',
						actions=[
							PostbackTemplateAction(
								label='幾Ａ幾Ｂ',
								text='!幾A幾B',
								data='action=buy&itemid=1'
							),
							MessageTemplateAction(
								label='幾Ａ幾Ｂ',
								text='!幾A幾B'
							),
							# URITemplateAction(
							# 	label='uri1',
							# 	uri='http://example.com/1'
							# )
						]
					),
					CarouselColumn(
						thumbnail_image_url='https://i.imgur.com/02b6MnB.jpg',
						title='機會命運',
						text='【機會、命運請選擇？】\n(一個會死、一個會活下來)',
						actions=[
							PostbackTemplateAction(
								label='機會命運',
								text='機會命運',
								data='action=buy&itemid=1'
							),
							MessageTemplateAction(
								label='機會命運',
								text='機會命運'
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
	else:
		print ("start finding library...")
		message = teach.get_key_response(user_message)

	if message != 0:
		return message
	else:
		return 0

def text_message(user_message):
	## ------ below are switch function ------	
	message = "default"
	if(user_message in ["!閉嘴"]):
		message = switch.switch_off()
	elif(user_message in ["!說話"]):
		message = switch.switch_still_on()

	# ------ below are event function ------		
	elif(user_message in ["即時排名","即時戰況",'排名','排行','分數','戰況','score']):
		message = event.event_board(2)
	elif(user_message in ["%數","%"]):
		message = event.event_board(3)
	elif(user_message in ['一位差']):
		message = event.event_board(4)
	elif(user_message in ['分數差']):
		message = event.event_board(5)
	elif(user_message in ['場數差']):
		message = event.event_board(6)
	elif(user_message in ["追擊時間","脫褲子"]):
		message = event.event_board(7)
	elif(user_message in ['時速']):
		message = event.event_board(8)
	elif(user_message in ['場速']):
		message = event.event_board(9)
	elif(user_message in ["活動進度",'進度']):
		message = event.event_progress()
	elif(user_message in ["剩餘時間"]):
		message = event.event_remain_time()
	elif(user_message.lower() in ["房號","room","rm","r"]):
		message = event.room_get()
	elif(user_message.lower().find("room1") == 0):
		message = event.room_update(user_message)
	elif(user_message.lower().find("room2") == 0):
		message = event.room_update2(user_message)
	elif(user_message.lower().find("r1") == 0):
		message = event.room_update(user_message)
	elif(user_message.lower().find("r2") == 0):
		message = event.room_update2(user_message)
	elif(user_message.lower().find("!fire") == 0):
		message = event.fire_calculator(user_message)
	elif(user_message.lower().find("!stone") == 0):
		message = event.stone_calculator(user_message)
	elif(user_message.lower() == "!pt"):
		message = event.percent_table()
	elif(user_message.lower().find("!lz") == 0):
		message = event.total_calculator(user_message)
	elif(user_message.lower().find("!ptstone") == 0):
		message = event.pt_stone(user_message)

	# ------ below are food function ------	
	elif(user_message in ["!抽食物"]):
		message = food.get_food_sheet(1)
	elif(user_message in ["!抽飲料"]):
		message = food.get_food_sheet(2)

	# ------ below are gacha function ------	
	elif(user_message.lower()  in ["!cgss單抽"]):
		message = "【CGSS 單抽結果】\n" + gacha.gacha_CGSS()
	elif(user_message.lower()  in ["!cgss十連","!cgss十抽","!cgss10連","!cgss10抽"]):
		message = "【CGSS 10連結果】\n" + gacha.ten_gacha_CGSS()
	elif(user_message.lower()  in ["!bgd單抽"]):
		message = "【BGD 單抽結果】\n" + gacha.gacha_BGD()
	elif(user_message.lower()  in ["!bgd十連","!bgd十抽","!bgd10連","!bgd10抽","!gbp十連","!gbp十抽","!gbp10連","!gbp10抽"]):
		message = "【BGD 10連結果】\n" + gacha.ten_gacha_BGD()
	elif(user_message.lower()   in ["!sc單抽"]):
		message = "【SC 單抽結果】\n" + gacha.multi_gacha_SC(1)
	elif(user_message.lower()  in ["!sc十連","!sc十抽","!sc10連","!sc10抽"]):
		message = "【SC 10連結果】\n" + gacha.multi_gacha_SC(10)

	# ------ below are game function ------	
	elif(user_message == "!終極密碼"):
		message = game.guess_number_set()
	elif(game.guess_number_mode == 1 and game.is_number(user_message)):
		message = game.guess_number(int(user_message))
	elif(user_message == "!幾A幾B"):
		message = game.guess_AB_set()
	elif(game.guess_AB_mode == 1 and game.is_numberAB(user_message)):
		message = game.guess_AB(user_message)
	elif(user_message.lower() == "abreset"):
		message = game.guess_AB_reset()

	# ------ below are find function ------	 
	elif(user_message.find("!機率") == 0):
		try:
			reply_message = user_message.split(" ",1)
			if reply_message[1] == "?":
				message = "【請依照範例輸入：】\n!機率 (想預測的事情)"
			else:
				message = "嗯... 我覺得 "+reply_message[1] + " 的機率是 "+ str(random.randint(0,101)) + " % !!!"
		except:
			message = "【請依照範例輸入：】\n!機率 (想預測的事情)"
	elif(user_message.find("!抽數字") == 0):
		try:
			reply_message = user_message.split(" ",1)		
			message = random.randint(1,int(reply_message[1]))
		except:
			message = "【請依照範例輸入：】\n!抽數字 (你的數字)\n(「1~你的數字」抽一個數字)"

	# ------ below are teach function ------	
	elif(user_message.find("!教育") == 0):
		message = teach.teach(user_message,0)
	elif(user_message.find("!調教") == 0):
		message = teach.teach(user_message,1)
	elif(user_message.find("!學圖") == 0):
		message = teach.teach_pic(user_message,0)
	elif(user_message.find("!智乃看圖片") == 0):
		message = teach.teach_pic(user_message,0)
	elif(user_message.find("!給智乃看圖") == 0):
		message = teach.teach_pic(user_message,1)
	elif(user_message.find("!智乃看圖圖") == 0):
		message = teach.teach_pic(user_message,2)
	# elif(user_message.find("!忘記") == 0):
	# 	forget_result = forget(user_message)
	# 	message = TextSendMessage(text=forget_result)
	# 	line_bot_api.reply_message(event.reply_token,message)

	# ------ below are note function ------	
	elif(user_message.lower().find("!addnote") == 0):
		message = note.add_note(user_message)
	elif(user_message.lower().find("!delnote") == 0):
		message = note.del_note(user_message)
	elif(user_message.lower() == "!shownote"):
		message = note.show_note()
	elif(user_message.lower().find("!restorenote") == 0):
		message = note.restore_note(user_message)
	elif(user_message.lower() == "!backupnote"):
		message = note.backup_note()

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


# notes 
	
#push message to one user
# line_bot_api.push_message(user_id, 
    # TextSendMessage(text='Hello World!'))
# push message to multiple users
# line_bot_api.multicast(['user_id1', 'user_id2'], 
    # TextSendMessage(text='Hello World!'))	