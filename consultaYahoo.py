# -*- coding: cp1252 -*-
'''
https://towardsdatascience.com/a-comprehensive-guide-to-downloading-stock-prices-in-python-2cd93ff821d4
á
'''
import yfinance as yf
import datetime
import time
import traceback
import pickle
import os

ontem = datetime.datetime.now()-datetime.timedelta(days=1)
ontemst = ontem.strftime("%Y-%m-%d")

ORG_EXT = 0
ORG_BRA = 1
ORG_CRP = 2
ORG_IBR = 3

intraday = False
consulta = True

apenas_novas = False

# 1 ano
consulta_padrao = False

# 5 anos
consulta_historico = True

lstConsulta = [ORG_BRA, ORG_EXT, ORG_CRP]
lstConsulta = [ORG_CRP]


# -------------------------------
def nomeok(nome):
    if '#' in nome or '-' in nome or len(nome)== 0 or not nome[0].isalpha():
        return False

    if '-' in nome or ' ' in nome or "+" in nome or '%' in nome:
        return False

    return True
# -------------------------------

def executa_consulta():    

    #for origem in [ORG_EXT]:
    for origem in lstConsulta:


        if origem == ORG_EXT:
            base = 'exterior'
        elif origem == ORG_BRA:    
            base='brasil'
        elif origem == ORG_CRP:    
            base = 'cripto'
        elif origem == ORG_IBR:    
            base = 'ibrx100'            
        else:
            print("erro de origem")
            quit()

        nomeacoes = 'acoes_%s.txt'%base
        dout = 'cotacoes/%s'%base

        try:
            os.makedirs(dout)
        except:
            pass


        try:
            acoes = eval(open(nomeacoes).read())
            
        except:
            print("organizando lista de acoes")
            acoes = open(nomeacoes).readlines()
            acoes = [a.rstrip() for a in acoes]
            acoes = [a for a in acoes if nomeok(a)]
            acoes = sorted(list(set(acoes)))
            #quit()
            open(nomeacoes,'wt').write(str(acoes))


            
        # limpa diretorio
        arqs= [a for a in os.listdir(dout) if 'csv' in a]
            
        if not intraday and not apenas_novas:
            for a in arqs:
                os.remove(dout+'/'+a)

        #acoes = ['RANI3']

        #acao = acoes[0]

        vhist = []

        if consulta:
            for acao in acoes:

                if apenas_novas:
                    if acao+'.csv' in arqs:
                        print(acao, "já disponível")
                        continue
                
                nome = acao
                if origem == ORG_BRA or origem == ORG_IBR:
                    nome = acao+'.SA'
                elif origem == ORG_CRP:
                    nome = nome+"-USD"

                try:
                    #vals = yf.download(nome, start='2020-01-01', progress=False)
                    if intraday:
                        vals = yf.download(nome, period='1d', interval='15m', progress=False)
                        vhist.append([acao, vals.iloc[-1]['Close'], vals.index[-1]])
                        print(vhist[-1])
                    elif consulta_padrao:    
                        vals = yf.download(nome, period='1y', interval='1d', progress=False)
                        #vals = yf.download(nome, period='5y', interval='1h', progress=False)
                        #vals = yf.download(nome, period='3mo', interval='1d', progress=False)
                        open('%s/%s.csv'%(dout,acao),'wb').write(vals.to_csv())
                        print(acao)
                        print(vals.iloc[-1])
                    elif consulta_historico:
                        vals = yf.download(nome, period='5y', interval='1d', progress=False)
                        open('%s/%s.csv'%(dout,acao),'wb').write(vals.to_csv())
                        print(acao)
                        print(vals.iloc[-1])
                        
                    else:
                        vals = yf.download(nome, period='2y', interval='1h', progress=False)
                        nome = '%s/%s-1h.csv'%(dout,acao)
                        open(nome,'wb').write(vals.to_csv())

                        vals = open(nome).readlines()
                        fout = open('%s/%s-1hh.csv'%(dout,acao),'wb')
                        dant = None
                        h=9
                        fout.write(vals[0]+'\n')
                        for v in vals[1:]:
                            w = v.rstrip().split(',')
                            if w[0]!= dant:
                                h = 10
                                dant = w[0]
                            else:
                                h=h+1

                            w[0] = w[0]+" %02d:00"%h   
                            fout.write(','.join(w) + '\n')
                        fout.close()

                        #break

                   
                except:
                    if intraday:
                        vhist.append([acao, "'-", "'-"])

                    print("falha lendo", acao)
                    print(traceback.format_exc())
                    
                time.sleep(1)

            pickle.dump(vhist, open('vhist_%s.pick'%base,'wb'))
            
        else:
            vhist = pickle.load(open('vhist_%s.pick'%base,'rb'))
            


        if intraday:
            fout = open('precos_%s.txt'%base,'wt')
            fout.write("TICKER\tULTVAL\tDTH\n")
            
            for v in sorted(vhist):
                if type(v[1]) != str:
                    fout.write('%s\t%4.2f\t%s\n'%(v[0],v[1],str(v[2])))
            fout.close()


#####################
if __name__ == "__main__":
    executa_consulta()
