


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

def get_food_sheet(key):
	global my_database_sheet_ID
	if key == 1:
		values = get_value_from_google_sheet(my_database_sheet_ID,'food!A2:A')
	elif key == 2:
		values = get_value_from_google_sheet(my_database_sheet_ID,'food!B2:B')
	if not values:
		print('No data found.')
	else:
		list_food = []
		for row in values:	
			list_food.append(row[0])
			
		random_food_index = random.randint(0,len(list_food)-1)
		return str(list_food[random_food_index])