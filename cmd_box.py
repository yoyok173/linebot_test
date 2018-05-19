
'''
def search_cmd(user_message):
	operations_str = [
	[["!閉嘴","!安靜","!你閉嘴","!你安靜"],switch_off()],
	[["!說話"],switch_still_on()],
	[["!使用說明書","!help","!說明書"],readme()],
	[["即時排名","即時戰況",'排名','分數','戰況','score'],event_board(2)],
	[["%數","%"],event_board(3)],
	[['分數差'],event_board(5)],
	[['場數差'],event_board(6)], 
	[["追擊時間","脫褲子","脫內褲","內褲","褲子"],event_board(7)],
	[['時速'],event_board(8)], 
	[['場速'],event_board(9)],
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