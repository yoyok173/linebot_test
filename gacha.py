
import random

BGD_namelist = [
'牛込りみ','山吹沙綾','戸山香澄','市ヶ谷有咲','花園たえ',
'上原ひまり','羽沢つぐみ','美竹蘭','宇田川巴','青葉モカ',
'白鷺千聖','若宮イヴ','丸山彩','大和麻弥','氷川日菜',
'氷川紗夜','宇田川あこ','湊友希那','白金燐子','今井リサ',
'北沢はぐみ','奥沢美咲','弦巻こころ','瀬田薫','松原花音']

SC_nameList = [
'風野灯織','八宮めぐる','櫻木真乃','月岡恋鐘',
'田中摩美々','幽谷霧子','三峰結華','白瀬咲耶',
'桑山千雪','大崎甘奈','大崎甜花','小宮果穂',
'杜野凛世','園田智代子','西城樹里','有栖川夏葉'
]

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

def multi_gacha_SC(number):
	sc_gacha_result = ""
	for i in range(number-1):
		sc_gacha_result += str(gacha_SC())
		sc_gacha_result += "\n"
	sc_gacha_result += str(gacha_SC_Last())
	return sc_gacha_result
