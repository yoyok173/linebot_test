import random


def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		pass

def is_numberAB(user_guess):
	try:
		float(user_guess)
		try:
			user_guess_numberlist = [user_guess[0],user_guess[1],user_guess[2],user_guess[3]]
		except
			pass

	except ValueError:
		pass

upperbound = 100
lowerbound = 0
target_number = 0
guess_number_mode = 0
someone_playing_guess = 0
def guess_number_set():
	global target_number,guess_number_mode,upperbound,lowerbound,someone_playing_guess
	if someone_playing_guess == 1:
		return " 請稍候~ 現在有人正在玩哦~ "
	else:
		guess_number_mode = 1
		someone_playing_guess = 1
		upperbound = 100
		lowerbound = 0
		target_number = random.randint(1,99)
		return " 【 終極密碼 】 \n遊戲設定完成！\n請輸入0~100的數字"

def guess_number(user_guess):
	global upperbound,lowerbound,target_number,guess_number_mode,someone_playing_guess
	if user_guess == target_number:
		someone_playing_guess = 0
		guess_number_mode = 0
		upperbound = 100
		lowerbound = 0
		target_number = 0
		return "恭喜！！！答案就是【"+str(user_guess)+"】！"
	elif (user_guess > target_number and user_guess < upperbound):
		upperbound = user_guess
		return str(lowerbound)+" ~ "+str(upperbound) + " 之間"
	elif (user_guess < target_number and user_guess > lowerbound):
		lowerbound = user_guess
		return str(lowerbound)+" ~ "+str(upperbound) + " 之間"

guess_AB_counter=0
guess_AB_mode=0
target_AB = ["a","a","a","a"]
someone_playing_AB = 0	
def guess_AB_set():
	global guess_AB_mode,target_AB,guess_AB_counter,someone_playing_AB
	if someone_playing_AB == 1:
		return " 請稍候~ 現在有人正在玩哦~ "
	else:
		guess_AB_mode = 1
		guess_AB_counter = 0
		someone_playing_AB = 1
		for i in range(4):
			target_AB[i] = str(random.randint(0,9))
			j=0
			while(j < i and i > 0):
				if target_AB[i] == target_AB[j]:
					target_AB[i] = str(random.randint(0,9))
					j=0
				else:
					j+=1
		print(target_AB)
		return " 【 幾A幾B 】 \n遊戲設定完成！\n請輸入您的四位數字\n(0~9不重複數字)"

def guess_AB(user_guess):
	global guess_AB_mode,target_AB,guess_AB_counter,someone_playing_AB
	guess_AB_counter += 1
	cntA = 0
	cntB = 0
	user_guess_numberlist = [user_guess[0],user_guess[1],user_guess[2],user_guess[3]]
	if user_guess_numberlist == target_AB:
		guess_AB_mode = 0
		guess_AB_counter = 0
		someone_playing_AB = 0
		target_AB = ["a","a","a","a"]
		return "恭喜！！！答案就是【"+str(user_guess)+"】！"
	for i in range(4):
		if user_guess_numberlist[i] == target_AB[i]:
			user_guess_numberlist[i] = "a"
			cntA+=1
		if user_guess_numberlist[i] in target_AB:
			cntB+=1
	if guess_AB_counter >= 10:
		return "【你們已經猜了 "+str(guess_AB_counter)+" 次】\n"+str(cntA)+" A "+str(cntB) + " B"+"\n不覺得有點太多了嗎？"
	else:
		return "【你們已經猜了 "+str(guess_AB_counter)+" 次】\n"+str(cntA)+" A "+str(cntB) + " B"

def guess_AB_reset():
	global guess_AB_counter,guess_AB_mode,target_AB,someone_playing_AB
	guess_AB_counter=0
	guess_AB_mode=0
	target_AB = ["a","a","a","a"]
	someone_playing_AB = 0	
	return "The AB game has been terminated, please restart the game."
