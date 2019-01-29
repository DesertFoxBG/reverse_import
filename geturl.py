import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

json_key = json.load(open('pythontosheets-229709-43bddc4cb237.json')) # json credentials you downloaded earlier
scope = ['https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope) # get email and key from creds

file = gspread.authorize(credentials) # authenticate with Google
sheet = file.open("Untitled spreadsheet").sheet1 # open sheet

sheet.update_cell(5, 1, '4')
all_cells = sheet.range('A1:D5')

print dir(all_cells)

print "r c v\n----------------"
for cell in all_cells:
	#print dir(cell)
	print str(cell.row) + ' ' + str(cell.col) + ' ' + cell.value

