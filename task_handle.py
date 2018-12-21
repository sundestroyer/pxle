# - coding: utf-8 --
from __future__ import print_function
import random
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import mailer
from datetime import datetime,timedelta
msg = {'sender' : "wtfshechka@gmail.com",
'subject':"WITF{}",
'msgHtml':'''УВАЖАЕМЫЕ УЧАСТНИКИ ИНТЕЛЛЕКТУАЛЬНОЙ ИГРЫ!<br><br>

Сегодня Московский университет МВД России имени В.Я. Кикотя проводит вторые интеллектуальные соревнования «Мультимедийные технологии (WiTF – Where is The Flag)» среди курсантов и слушателей образовательных учреждений МВД России.
Организационный комитет рад приветствовать Вас на виртуальной площадке соревнований!
Проведение данных соревнований должно способствовать повышению качества образовательного процесса по вопросам, связанным с изучением информационных технологий, а также повышению практической направленности обучения курсантов и слушателей образовательных учреждений МВД России.
Кроме того, в качестве задач проведения соревнований предлагается определить: установление дружеской атмосферы, повышение сплоченности коллективов курсантов и слушателей, повышение навыков общения и работы в командах, повышение эрудиции обучающихся, обмен ценным опытом, как это было во время проведения первых соревнований.
Организационный комитет желает всем участникам соревнований достичь высоких результатов при решении прикладных задач в рамках этих соревнований!<br>
Код вашей команды:{}<br>
Задания:https://drive.google.com/drive/folders/11w1u6byjniEs7BO-2yD5du-MFsp12_Y3?usp=sharing<br>
Форма отправки ответов:https://goo.gl/forms/UyIqVC9MRyxkdbBH2<br>
Результаты:https://docs.google.com/spreadsheets/d/1rsz9WAPCAnWggQ5nB9dgMqhwHtgi57p73mLNA88r19s/edit?usp=sharing
''',
'msgPlain':'''УВАЖАЕМЫЕ УЧАСТНИКИ ИНТЕЛЛЕКТУАЛЬНОЙ ИГРЫ!

Сегодня Московский университет МВД России имени В.Я. Кикотя проводит вторые интеллектуальные соревнования «Мультимедийные технологии (WiTF – Where is The Flag)» среди курсантов и слушателей образовательных учреждений МВД России.
Организационный комитет рад приветствовать Вас на виртуальной площадке соревнований!
Проведение данных соревнований должно способствовать повышению качества образовательного процесса по вопросам, связанным с изучением информационных технологий, а также повышению практической направленности обучения курсантов и слушателей образовательных учреждений МВД России.
Кроме того, в качестве задач проведения соревнований предлагается определить: установление дружеской атмосферы, повышение сплоченности коллективов курсантов и слушателей, повышение навыков общения и работы в командах, повышение эрудиции обучающихся, обмен ценным опытом, как это было во время проведения первых соревнований.
Организационный комитет желает всем участникам соревнований достичь высоких результатов при решении прикладных задач в рамках этих соревнований!
Код вашей команды:{}
Задания:https://drive.google.com/drive/folders/11w1u6byjniEs7BO-2yD5du-MFsp12_Y3?usp=sharing
Форма отправки ответов:https://goo.gl/forms/UyIqVC9MRyxkdbBH2
Результаты:https://docs.google.com/spreadsheets/d/1rsz9WAPCAnWggQ5nB9dgMqhwHtgi57p73mLNA88r19s/edit?usp=sharing
'''}
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
tm_CSV = 'teams_id.txt'
def get_mails(service):
    rng = 'B:B'
    result = service.spreadsheets().values().get(spreadsheetId='1UgyggiartvbdFPo9kYwwsdNNkuldYSfW0pZ6SMZqVDo', range=rng).execute()
    mails = [item[0] for item in result['values'] if item != []][1:]
    return genID(mails,service)
#def genCSV(file):
def genID(teams,service):
    alph = ('a','b','c','d','e','f','g','h','j','4','5','6','7','8','9','t','y','u','1','2','3')
    k = [(''.join(random.sample(alph,6)),item) for item in teams]
    values = [[item[0] for item in k],[]]
    body = {'majorDimension':'COLUMNS','values':values}
    result = service.spreadsheets().values().update(
    spreadsheetId='1rsz9WAPCAnWggQ5nB9dgMqhwHtgi57p73mLNA88r19s', range='A2:A',
    valueInputOption='RAW', body=body).execute()
    return k




def get_res_cells(service):
    import string
    with open(tm_CSV,'r') as f:
        codes = [item.split(':')[0] for item in f.read().split('\n') if item != '']
        teams = dict([(item,str(n+2)) for n,item in enumerate(codes)])
        rng = 'B1:1'
        result = service.spreadsheets().values().get(spreadsheetId='1rsz9WAPCAnWggQ5nB9dgMqhwHtgi57p73mLNA88r19s', range=rng).execute()['values'][0]
        tasks = dict([(item,string.ascii_uppercase[k+1]) for k,item in enumerate(result[:-1])])
        return (teams,tasks)
def main():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
#comment from here
    #id_lst = get_mails(service)
    #with open(tm_CSV,'w') as f:
       # for item in id_lst:
          #  f.write('{}:{}\n'.format(item[0],item[1]))
#to here
    #from test import make_srt
    #make_srt()
    sorted_csv = 'srtteams.txt'
    with open(sorted_csv,'r') as f:
        for item in f:
            item = item.split(':')
            mailer.SendMessage(msg['sender'],item[1],msg['subject'],msg['msgHtml'].format(item[0]),msg['msgPlain'])



if __name__ == '__main__':
    main()
