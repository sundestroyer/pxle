# - coding: utf-8 --
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from time import sleep
from task_handle import get_res_cells
#sheet where results stores
result_sheet = '1rsz9WAPCAnWggQ5nB9dgMqhwHtgi57p73mLNA88r19s'
#response wrom google forms
answer_sheet = '1L1zwdlYdpPOBg_m_5PPmZ4y7NpzLu-q8nUAlI3AZx0o'
def get_dict(path):
    with open(path,'r') as f:
        flags_dict = {item.split(':')[0]:(item.split(':')[1],item.split(':')[2]) for item in f}
        return flags_dict
# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
def accept_flag(answer,service):
    #get cells from files
    l = get_res_cells(service)
    tms = l[0]
    tasks = l[1]
    #make cells range
    rng = '{}:{}'.format(tasks[answer[1]]+tms[answer[0]],tasks[answer[1]]+tms[answer[0]])
    #compare google range
    values = [[int(answer[1][-3:])],[]]
    body = {'values':values}
    #update cells
    result = service.spreadsheets().values().update(
    spreadsheetId=result_sheet, range=rng,
    valueInputOption='RAW', body=body).execute()


def check_flag(answer,flags_dict,service):
    #check if flag right
    if flags_dict[str(answer[1])][0] == answer[2]:
        #past flag in table
        accept_flag(answer,service)


def main():
    path = r'flags_dict.txt'
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    #parse flags csv
    flags_dict = get_dict(path)
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    line = 66
    while True:
        #check_loop
        #declare_current line
        rng = 'B{}:D{}'.format(line,line)
        #get curr line value
        result = service.spreadsheets().values().get(spreadsheetId=answer_sheet, range=rng).execute()
        #check it for answer
        if 'values' in result:
            #past flag
            check_flag(result['values'][0],flags_dict,service)
            print(line)
            line+=1
        #wait for flag
        else:
            sleep(20)
    print('{0}'.format(result))



if __name__ == '__main__':
    main()
