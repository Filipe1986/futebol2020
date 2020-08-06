# -*- coding: UTF-8 -*-
from flask_cors import CORS
import requests
import logging
import sys
import json
from lxml import html    
from datetime import datetime, timedelta
import time
import os.path as path

ano = 2015
mes = 12
dia = 31
date = datetime(ano, mes, dia)
FILE_NAME = "".join([ str(date.month), '-', str(date.year), '.csv'])
FILE_LOG  = "".join([ str(date.month), '-', str(date.year), '-log.csv'])

url = 'https://bid.cbf.com.br/a/bid/carregar/json/'

params = {'dt_pesquisa':'31/12/2019','tp_contrato':'TODOS'}


headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://bid.cbf.com.br',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://bid.cbf.com.br/',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': 'PHPSESSID=krhmtcp4n4jqook4k72e4gdu11; _ga=GA1.3.35946942.1596113948; _gcl_au=1.1.1283635082.1596119756; _fbp=fb.2.1596119757146.861450703; _hjid=f571adf5-28cc-4a4a-b468-76bf54135f33; _gid=GA1.3.1152925700.1596315779; _gat=1; _gali=AguardeButton'
}

def req(params):
    try:
        return requests.post(url, headers=headers, data=params)
    except Exception :
        print('Except: ' + str(Exception) + dateFormatted)
        erroFile = open(FILE_LOG, "a" ,encoding='utf8')
        erroFile.write(dateFormatted + '; Except ;' + str(Exception)  + '\n', encoding='utf8')
        erroFile.close()
        return {'codigo_status' : 0, 'content': ''}


while date.year == ano:
    
    dateFormatted = date.strftime("%d/%m/%Y")
    params['dt_pesquisa'] = dateFormatted
    time.sleep(1)

    FILE_NAME = "".join([ str(date.month), '-', str(date.year), '.csv'])
    FILE_LOG  = "".join([ str(date.month), '-', str(date.year), '-log.csv'])

    if(not path.exists(FILE_NAME)):
        open(FILE_NAME, "x")
    if(not path.exists(FILE_LOG)):
        open(FILE_LOG, "x")

    r = req(params)
    if(r.status_code == 0):
        continue

    print('Código HTTP: ' + str(r.status_code) +' - ' +dateFormatted )
    if(r.status_code == 200 and len(r.content) > 10):
        dados = r.json()['dados']

        dados_json = html.fromstring(dados)

        htmlNum = dados_json.xpath('//div/strong/following-sibling::text()')
        htmlf = dados_json.xpath('//div[@class="modal fade"]/div/div')
        
        f = open(FILE_NAME, "r", encoding='utf8')
        if(not f.readline() or f.readline() == ''):
            f = open(FILE_NAME, "a" ,encoding='utf8')
            f.write("Jogador; Inscricao; Contrato; N; Inicio; Nascimento; dt_inscricao; clube\n")
            f.close()

        f = open(FILE_NAME, "a", encoding='utf8')

        print('Num: ' + str(htmlNum[0]))
        checkSize = len(htmlf)
        print('len: ' + str(checkSize))

        if(int(htmlNum[0]) == int(checkSize)):
            for i in htmlf:
                s = i.xpath('.//div[@class="modal-header"]/h4/text()')[0] + "; " \
                    + i.xpath('.//div[@class="modal-body"]/div/div[2]/p/text()')[0] + "; " \
                    + i.xpath('.//div[@class="modal-body"]/div/div[2]/p/text()')[1] + "; " \
                    + i.xpath('.//div[@class="modal-body"]/div/div[2]/p/text()')[2] + "; " \
                    + i.xpath('.//div[@class="modal-body"]/div/div[2]/p/text()')[3] + "; " \
                    + i.xpath('.//div[@class="modal-body"]/div/div[2]/p/text()')[4] + "; " \
                    + i.xpath('.//div[@class="modal-body"]/div/div[2]/p/text()')[5] + "; " \
                    + i.xpath('./div[@class="modal-body"]/div/div[2]/div/div/p/text()')[0] + "\n"
                f.write(s)
            print('Sucesso: ' +  dateFormatted)
            erroFile = open(FILE_LOG, "a" ,encoding='utf8')
            erroFile.write(dateFormatted + '; ' + str(htmlNum[0]) + '; '+  str(checkSize) + '\n')
            erroFile.close()
            f.close()
        else:
            print('Erro de qtd: ' +  dateFormatted)
            print(r)
            erroFile = open(FILE_LOG, "a" ,encoding='utf8')
            erroFile.write(dateFormatted + '; ' + str(htmlNum[0]) + '; '+  str(checkSize)+ '\n')
            erroFile.close()
    else:
        print('Erro: ' +  dateFormatted)
        print(r)
        erroFile = open(FILE_LOG, "a" ,encoding='utf8')
        erroFile.write(dateFormatted + '; '+ str(r.status_code) + '; ' + str(r.content) + '\n')
        erroFile.close()
    date = date - timedelta(days=1)
    

print("Fim")