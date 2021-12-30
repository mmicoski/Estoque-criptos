# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 21:47:35 2018

@author: mmico
"""

#REST post in Python
#https://techietweak.wordpress.com/2015/03/30/http-restful-api-with-python-requests-library/
# AlphaVantage
# https://www.alphavantage.co/documentation/

import requests
import json
import traceback
import time

import trade_util as tut

keyAlpha = open('../keyAlpha.txt').read()
url_intraday = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=%s&interval=%dmin&apikey=%s&datatype=json'
url_daily = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&apikey=%s&datatype=json'
url_daily_csv = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&apikey=%s&datatype=csv'

#url_cripto_daily_csv = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=%s&market=BRL&apikey=%s&datatype=csv'
url_cripto_daily_csv = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=%s&market=USD&apikey=%s&datatype=csv'


url_consulta_ref = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=OIBR3&interval=60min&apikey=XOJE8KQJBF3YPX98&datatype=json'
url_consulta_ref_cripto = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=ETH&market=BRL&apikey=XOJE8KQJBF3YPX98'

nome = 'alpha'

dadosacao = [
"1. open",
"2. high",
"3. low", 
"4. close",
"5. volume",        
        ]

dadout = ["DATA","CODNEG","PREABE","PREMAX","PREMIN","PREULT","VOLTOT"]

resUltConsulta = [None, None]

def consultaAcaoIntraday(nome = 'PETR4', intervalo_min=60):
    global resUltConsulta
    
    url_consulta = url_intraday%(nome, intervalo_min, keyAlpha)
    
    r = requests.get(url_consulta)


    resUltConsulta[0] = r
    resUltConsulta[1] = r.text
    
                  
    try:
        oj = json.loads(r.text)
    except:
        print("Erro lendo json")
        print(r.text)
        print(traceback.format_exc())
        return None
        
    vals = []
    vals.append(dadout)
    keys = list(oj.keys())
    
    if len(keys) < 2:
        print("Erro na consulta de ", url_consulta)
        print(r)
        print(r.text)
        return None
    
    ts = [i for i in range(len(keys)) if 'Time Series' in keys[i]]
    if len(ts) != 1:
        print("Erro: sem dados na consulta de ", url_consulta)
        print(r)
        print(r.text)
        quit()


    its = ts[0]
    
    symbol = oj[keys[1-its]]["2. Symbol"]
    dados = oj[keys[its]]
        
    for dh in sorted(list(dados)):
        dadosper = dados[dh]
        vper = [dh, symbol]
        vper.extend([dadosper[x] for x in dadosacao])
        vals.append(vper)
        

    return vals


def consultaAcaoDaily(nome = 'PETR4'):
    global resUltConsulta
    
    url_consulta = url_daily%(nome, keyAlpha)
    
    r = requests.get(url_consulta)


    resUltConsulta[0] = r
    resUltConsulta[1] = r.text
    
                  
    try:
        oj = json.loads(r.text)
        
    except:
        print("Erro lendo json")
        print(r.text)
        print(traceback.format_exc())
        return None
        
    vals = []
    vals.append(dadout)
    keys = list(oj.keys())
    
    if len(keys) < 2:
        print("Erro na consulta de ", url_consulta)
        print(r)
        print(r.text)
        return None
    
    ts = [i for i in range(len(keys)) if 'Time Series' in keys[i]]
    if len(ts) != 1:
        print("Erro: sem dados na consulta de ", url_consulta)
        print(r)
        print(r.text)
        quit()


    its = ts[0]
    
    symbol = oj[keys[1-its]]["2. Symbol"]
    dados = oj[keys[its]]
        
    for dh in sorted(list(dados)):
        dadosper = dados[dh]
        vper = [dh, symbol]
        vper.extend([dadosper[x] for x in dadosacao])
        vals.append(vper)
        

    return vals


def consultaAcaoDaily_csv(nome = 'PETR4'):
    global resUltConsulta
    
    if tipo == tut.TIPO_CRIPTO:
        url_consulta = url_cripto_daily_csv%(nome, keyAlpha)
    else:
        url_consulta = url_daily_csv%(nome, keyAlpha)
    
    r = requests.get(url_consulta)


    resUltConsulta[0] = r
    resUltConsulta[1] = r.text
    
    vals = [v.rstrip() for v in r.text.split('\n')]
    
    return vals

        
        
# ================================================
if __name__ == '__main__':      
    
    if 0:
        ret = consultaAcaoDaily_csv('CZZ')
    
        if ret:
            print(ret[0])
            print(ret[1])
            print(ret[-1])
    if 0:
    
        nome = 'AALR3.SA'
        url_consulta = url_daily_csv%(nome, keyAlpha)
        
        r = requests.get(url_consulta)
    
    
        resUltConsulta[0] = r
        resUltConsulta[1] = r.text
        
    
        oj = json.loads(r.text)
        
        open('test.txt','wt').write(str(oj))
        
        for k in oj:
            print(k)
            
        keys = list(oj.keys())
        for dh in oj[keys[1]]:
            print(dh)



    if 1:
        ''' CONSULTA E SALVA EM DISCO '''
        import os
        import datetime
        import time
        
        ontem = datetime.datetime.now()-datetime.timedelta(days=1)
        ontemst = ontem.strftime("%Y-%m-%d")
        
#        tipo = tut.TIPO_BRASIL  # brasil
#        tipo = tut.TIPO_EXTERIOR  # exterior
        tipo = tut.TIPO_CRIPTO  # cripto        
        
        #exterior = False    
    
        if tipo == tut.TIPO_EXTERIOR:
            acoes = eval(open('acoes_exterior.txt','rt').read())
            dirout = 'cotacoes/exterior'
        elif tipo == tut.TIPO_BRASIL:
            acoes = eval(open('acoes_brasil.txt','rt').read())
            dirout = 'cotacoes/brasil'
        elif tipo == tut.TIPO_CRIPTO:
            acoes = eval(open('acoes_cripto.txt','rt').read())
            dirout = 'cotacoes/cripto'
        else:
            raise ValueError("Tipo %d desconhecido"%tipo)            


        #acoes = ['AALR3', 'BMGB4','BRKM5','CCPR3','HBOR3','LINX3','MGLU3','MILS3','RBRR11','SQIA3','VILG11','VIVT4']
        try: os.makedirs(dirout)
        except: pass

            
        print(len(acoes),"acoes")

        st = 'PETR4.SA'
        st = acoes[0]
        falhas = []

        for st in acoes:
            print(datetime.datetime.now().strftime('%H:%M:%S'), st)        
            nome = st
            if tipo == tut.TIPO_BRASIL:
                nome = st+'.SA'
                
            vals = consultaAcaoDaily_csv(nome)
            
            err = len([v for v in vals if 'error' in v.lower()]) > 0
            

            if vals and not err:
                open('%s/%s.csv'%(dirout,st),'wt').write('\n'.join(vals))
                ultdata = vals[1].split(',')[0]
                if ultdata < ontemst:
                    print(st, "dados antigos: ultdata =", ultdata)
                
            else:
                print("falha")
                falhas.append(st)

            time.sleep(15)

        
        print(len(falhas), 'não lidas')

    if 0:
        import os
        import datetime
        try: os.mkdir('cotacoes')
        except: pass
        
        acoes = eval(open('acoes.txt','rt').read())
        print(len(acoes),"acoes")

        returns = []

        st = 'PETR4.SA'
        falhas = []

        for st in acoes[:1]:
            print(datetime.datetime.now().strftime('%H:%M:%S'), st)        
            vals = consultaAcaoDaily(st+'.SA')

            if vals:
                open('cotacoes/%s.txt'%st,'wt').write(str(vals))
                
                dias = [v[0].split() for v in vals]
                du = {d[0]:1 for d in dias[1:]}
                dus = sorted(du.keys())
                
                phoje = [d for d in vals if d[0].split()[0] == dus[-1]]
                pontem = [d for d in vals if d[0].split()[0] == dus[-2]]
                ret = float(phoje[0][2])/float(pontem[0][2])
                print(ret)
                returns.append([st, ret])
            else:
                print("falha")
                falhas.append(st)

        

        
        print(len(falhas), 'não lidas')
        rets = sorted(returns, key=lambda x:x[1])
        print('\nRecomendadas')
        for r in rets[:9]:
            print(r)
        
          


    if 0:
        nome = 'PETR4.SA'
        intervalo_min=60
        url_consulta = url%(nome, intervalo_min, keyAlpha)
        
        r = requests.get(url_consulta)


        resUltConsulta[0] = r
        resUltConsulta[1] = r.text
        
                      
        try:
            oj = json.loads(r.text)
        except:
            print("Erro lendo json")
            print(r.text)
            print(traceback.format_exc())
            quit()
            
        vals = []
        vals.append(dadout)
        keys = list(oj.keys())
        
        if len(keys) < 2:
            print("Erro na consulta de ", url_consulta)
            print(r)
            print(r.text)
            quit()

        its=0
        ts = [i for i in range(len(keys)) if 'Time Series' in keys[i]]
        if len(ts) != 1:
            print("Erro: sem dados na consulta de ", url_consulta)
            print(r)
            print(r.text)
            quit()


        its = ts[0]
        
        symbol = oj[keys[1-its]]["2. Symbol"]
        dados = oj[keys[its]]
        for dh in sorted(list(dados)):
            dadosper = dados[dh]
            vper = [dh, symbol]
            vper.extend([dadosper[x] for x in dadosacao])
            vals.append(vper)


if 0:
    acoes = open('acoesinteresse.txt').readlines()
    acoes = sorted(list(set([a.rstrip() for a in acoes])))
    open('acoes_brasil.txt','wt').write(str(acoes))
