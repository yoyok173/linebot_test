
notebook_content=[]

def add_note(user_message):
	try:
		split = user_message.split(" ",1)
		content = split[1]
	except:
		return "【請依照範例輸入：】\n!addnote (內容)"
	
	notebook_content.append(content)
	return "新增筆記成功！"

def show_note():
	if len(notebook_content) == 0:
		return "筆記本內容為空！"
	message = ""
	for i in range(len(notebook_content)):
		message += str(i+1)
		message += ")  "
		message += notebook_content[i]
		if i < len(notebook_content):
			message += "\n"
	return message

def del_note(user_message):
	try:
		split = user_message.split(" ",1)
		content_key = int(split[1])-1
	except:
		return "【請依照範例輸入：】\n!delnote (第幾則筆記)\n請先用!show查看筆記內容】"
	
	try:
		del notebook_content[content_key]
		return "刪除筆記成功！"
	except:
		return "刪除筆記失敗！請確定有該則筆記！"

def restore_note(user_message):
	try:
		split = user_message.split(" ",1)
		restore_content = split[1]
	except:
		return "【請依照範例輸入：】\n!restore (筆記備份內容)"
	try:
		split = restore_content.split(",",)
		for i in range(len(split)):
			notebook_content.append(split[i])
		return "筆記還原成功！"
	except:
		return "筆記還原失敗！請再確認格式是否正確！"


def backup_note():
	message = ""
	for i in range(len(notebook_content)):
		message += notebook_content[i]
		if i < len(notebook_content)-1:
			message += ","
	return "筆記備份成功！\n【請妥善保存以下內容：】\n"+message

