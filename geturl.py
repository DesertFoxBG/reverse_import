import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import sys
import time
import re

json_key = json.load(open('pythontosheets-229709-43bddc4cb237.json')) # json credentials you downloaded earlier
scope = ['https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope) # get email and key from creds

file = gspread.authorize(credentials) # authenticate with Google
sheet = file.open("Untitled spreadsheet") # open spreadsheet

print sheet.worksheets()


#if sheet.worksheets < 2:
#styles = sheet.add_worksheet(title = "styles", rows = '1000', cols = '10')
	
def pasteCsvCotn(content, sheet, cell):
    '''
    csvFile - path to csv file to upload
    sheet - a gspread.Spreadsheet object
    cell - string giving starting cell, optionally including sheet/tab name
      ex: 'A1', 'MySheet!C3', etc.
    '''

    wks = sheet.sheet1
    (firstRow, firstColumn) = gspread.utils.a1_to_rowcol(cell)

    body = {
        'requests': [{
            'pasteData': {
                "coordinate": {
                    "sheetId": wks.id,
                    "rowIndex": firstRow-1,
                    "columnIndex": firstColumn-1,
                },
                "data": content,
                "type": 'PASTE_NORMAL',
                "delimiter": ';',
            }
        }]
    }

    return sheet.batch_update(body)

def pasteCsvStyle(style, sheet, cell):
    stl = sheet.worksheet('styles')
    (firstRow, firstColumn) = gspread.utils.a1_to_rowcol(cell)

    body = {
        'requests': [{
            'pasteData': {
                "coordinate": {
                    "sheetId": stl.id,
                    "rowIndex": firstRow-1,
                    "columnIndex": firstColumn-1,
                },
                "data": style,
                "type": 'PASTE_NORMAL',
                "delimiter": '\n',
            }
        }]
    }

    return sheet.batch_update(body)

def pasteCsvHierarchy(hierarchy, sheet, cell):
    hie = sheet.worksheet('hierarchy')
    (firstRow, firstColumn) = gspread.utils.a1_to_rowcol(cell)

    body = {
        'requests': [{
            'pasteData': {
                "coordinate": {
                    "sheetId": hie.id,
                    "rowIndex": firstRow-1,
                    "columnIndex": firstColumn-1,
                },
                "data": hierarchy,
                "type": 'PASTE_NORMAL',
                "delimiter": '\n',
            }
        }]
    }

    return sheet.batch_update(body)

def pasteCsvPages(pages, sheet, cell):
    pg = sheet.worksheet('hierarchy')
    (firstRow, firstColumn) = gspread.utils.a1_to_rowcol(cell)

    body = {
        'requests': [{
            'pasteData': {
                "coordinate": {
                    "sheetId": pg.id,
                    "rowIndex": firstRow-1,
                    "columnIndex": firstColumn-1,
                },
                "data": pages,
                "type": 'PASTE_NORMAL',
                "delimiter": ',',
            }
        }]
    }

    return sheet.batch_update(body)

contents = open(str(sys.argv[1]), 'r')
cont = contents.read()
cont = cont.split('\n->\n')
#print cont

classes = open(str(sys.argv[2]), 'r')
cl = classes.read()
cl = cl.split('\n->\n')
#print cl
print len(cl)
print len(cont)

styles = open(str(sys.argv[3]), 'r')
st = json.load(styles)
#print st

cont_to_send = ''
class_to_send = '0001_00000300\n'
nums_class_to_send = ''
cont_class_to_send = ''

for count in range(0, len(cont)):
    cont_to_put = cont[count].replace('\n', '')
    print cont_to_put + '\n-----------------------------------------------------------------------------------------------------------------------------------------------------------'
    cont_to_send += cl[count] + ';' + cont_to_put + '\n'

for count in range(0, len(cl)):
    class_to_send += cl[count] + '\n'

for count in range(0, len(cl)):
    nums_class_to_send += str(count + 1) + '\n'

for count in range(0, len(cl)):
    cont_class_to_send += 'page ' + str(count + 1) + ','

style = ''
content = ''
name = ''

for count in range(0, len(cont)):
    json_object = st['jsonObject'][count]
    #print json_object
    for c in range (0, len(json_object)):
        json_el = json_object[c]
        json_el = str(json_el)
        json_el = re.sub('[u]', '', json_el)
        json_el = re.sub("[']", '', json_el)

        if '{' in json_el:
            content = json_el
        else:
            name = json_el

        if name != '' and content != '':
            style += '.' + name + ' ' + content + '\n'
            name = ''
            content = ''

style = style.replace(',', ';')

to_be_replaced = '"'
replace_with = "'"

cont_to_send = cont_to_send.replace(to_be_replaced, replace_with)
print cont_to_send
print sheet.id + '\n'

pasteCsvCotn('0001_00000300;Hello World!\n', sheet, 'A2') # ,
pasteCsvCotn(cont_to_send, sheet, 'A3') # ,
pasteCsvCotn('en', sheet, 'B1') # ,
pasteCsvPages(cont_class_to_send, sheet, 'B1') # ,
pasteCsvHierarchy(nums_class_to_send, sheet, 'A2') # \n
pasteCsvHierarchy(class_to_send, sheet, 'B2') # \n
pasteCsvStyle(style, sheet, 'A1') # \n