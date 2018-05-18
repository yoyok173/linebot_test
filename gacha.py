
import random

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