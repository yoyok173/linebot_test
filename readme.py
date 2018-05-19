

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

def readme():
	return TemplateSendMessage(
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
							text='!help',
							data='action=buy&itemid=1'
						),
						MessageTemplateAction(
							label='readme',
							text='!help'
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
					text='!教育/調教、!看圖、!智乃看圖片、!給智乃看圖、!智乃看圖圖、〖修復中〗!忘記',
					actions=[
						PostbackTemplateAction(
							label='學習文字',
							text='!教育 ?',
							data='action=buy&itemid=1'
						),
						MessageTemplateAction(
							label='學習圖片',
							text='!學圖 ?'
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
						PostbackTemplateAction(
							label='機率',
							text='!機率 ?',
							data='action=buy&itemid=1'
						),
						MessageTemplateAction(
							label='抽數字',
							text='!抽數字 ?'
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
							label='終極密碼',
							text='!終極密碼',
							data='action=buy&itemid=1'
						),
						MessageTemplateAction(
							label='幾A幾B',
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
					title=' - 【不知幹嘛類】 - ',
					text='貼圖辣、母湯、母湯電影版',
					actions=[
						PostbackTemplateAction(
							label='貼圖辣',
							text='貼圖辣',
							data='action=buy&itemid=1'
						),
						MessageTemplateAction(
							label='貼圖辣',
							text='貼圖辣'
						),
						# URITemplateAction(
						# 	label='uri1',
						# 	uri='http://example.com/1'
						# )
					]
				),
				CarouselColumn(
					thumbnail_image_url='https://i.imgur.com/02b6MnB.jpg',
					title=' - 【如果覺得太吵的話】 -',
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
					title=' - 【如果壞掉了要維修】 - ',
					text='!壞掉啦、呼叫四月、呼叫工程師',
					actions=[
						PostbackTemplateAction(
							label='壞掉啦！！！',
							text='呼叫工程師',
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