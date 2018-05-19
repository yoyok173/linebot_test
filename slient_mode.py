

from linebot.models import (
	MessageEvent, TextMessage, TextSendMessage,
)

import switch as switch

def slient_mode(user_message,event):
	if(user_message == "!說話"):
		switch.mode = 1 
		return = TextSendMessage(text='沒問題 ^_^，我來陪大家聊天惹，但如果覺得我太吵的話，請跟我說 「!閉嘴」 > <')
	elif(user_message == "!閉嘴"):
		switch.mode = 0
		return TextSendMessage(text='我已經閉嘴了 > <  (小聲)')
