# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 16:13:42 2021

@author: mmico
"""

import os
import pandas as pd
import json
import datetime

class HistoricoCotacao:
    ''' Guarda historico das criptomoedas em USD, a partir de arquivos obtidos
        dos sites
          https://www.alphavantage.co
          https://www.coingecko.com
        
        Guarda historico do dolar (USD) obtido do Banco Central do Brasil
          https://www.bcb.gov.br/estabilidadefinanceira/historicocotacoes
    
    '''
    def __init__(self, dirini=None):
        self.dirini = dirini
        self.precoCriptoUsd = {}
        self.precoDolarBrlCompra = {}
        self.precoDolarBrlVenda = {}
        
        if dirini is None:
            # le previamente salvo
            self.precoCriptoUsd = json.load(open("../cotacao_cripto.json","rt"))
            
        else:
            # le das consultas aos sites
            self.leHistoricoCripto()
        
    # --------------------
    def leHistoricoCripto(self):
        ''' le historico de valores das criptos, esperando valor em USD '''
        
        arqs = [a for a in os.listdir(self.dirini) if 'csv' in a]
        print("HistoricoCripto lendo historico de %d criptos"%len(arqs))
        
        for i,a in enumerate(arqs):
            regs = pd.read_csv(self.dirini+'/'+a, sep=',')
            nome = a
            if '-' in a:
                # formato CoinGecko
                nome = a.split('-')[0].upper()
                self.precoCriptoUsd[nome] = {regs.iloc[i]['snapped_at'].split()[0]:
                      regs.iloc[i]['price'] for i in range(len(regs))}
                    
            else:
                # formato AlphaVantage
                nome = a.split('.')[0]
                self.precoCriptoUsd[nome] = {regs.iloc[i]['timestamp']:
                      regs.iloc[i]['open (USD)'] for i in range(len(regs))}
                    
            
            if i%10 == 0:
                print("\r%d/%d "%(i,len(arqs)), end='')
                
        print("\r%d/%d"%(len(arqs),len(arqs)))


    # --------------------
    def leHistoricoDolar(self, nomearq):
        ''' le historico de valores do dolar de compra e venda do BCB '''
        
        regs = pd.read_csv(nomearq, sep='\t', decimal=',')
        
        self.precoDolarBrlCompra = {
                datetime.datetime.strptime(regs.iloc[i]['Data'], '%d/%m/%Y').strftime('%Y-%m-%d') :
                    regs.iloc[i]['R$Compra'] 
                    for i in range(len(regs))
                }
        
        self.precoDolarBrlVenda = {
                datetime.datetime.strptime(regs.iloc[i]['Data'], '%d/%m/%Y').strftime('%Y-%m-%d') :
                    regs.iloc[i]['R$Venda'] 
                    for i in range(len(regs))
                }
        
                   
            

            
    # --------------------
    def salva_json(self):
        json.dump(self.precoCriptoUsd, open("../cotacao_cripto_usd.json","wt"))
        json.dump(self.precoDolarBrlCompra, open("../cotacao_usdbrl_compra.json","wt"))
        json.dump(self.precoDolarBrlVenda, open("../cotacao_usdbrl_venda.json","wt"))
        
        
        
    # --------------------
    def consultaCripto(self, nome, data):
        dad = self.precoCriptoUsd.get(nome, None)

        if dad is None:
            print("HistoricoCripto: sem dados para", nome)
            return None

        valor = dad.get(data, None)
        if valor is None:
            print("HistoricoCripto: sem data %s para %s"%(data, nome))
            return None
        
        return valor
        
    # --------------------
    def consultaDolar(self, data, compra=True):
        
        if compra: 
            dicc = self.precoDolarBrlCompra
        else:
            dicc = self.precoDolarBrlVenda
        
        if data in dicc:
            return dicc[data]
        
        else:
            #(regs.iloc[i]['Data'], '%d/%m/%Y').strftime('%Y-%m-%d')
            dataini = datetime.datetime.strptime(data, '%Y-%m-%d')
            for diasAntes in range(1,10):
                dbusca = dataini-datetime.timedelta(days=diasAntes)
                dbuscast = dbusca.strftime('%Y-%m-%d')
                if dbuscast in dicc:
                    print("usando dolar de %s para %s"%(dbuscast, data))
                    return dicc[dbuscast]

        return None       
        
            
        
        
        
# =====================
if __name__ == '__main__':
    
    dirini = 'cotacoes/cripto'
    hc = HistoricoCotacao()
    
    hc.leHistoricoDolar('../cotacoes/USDBRL_BCB.tsv')
    
    data = '2021-08-01'
    val = hc.consultaCripto('AAVE',data)
    valusd = hc.consultaDolar(data, compra=True)
    print(val, valusd)    
    
    
    
#    nomearq = '../cotacoes/USD.tsv'
#    regs = pd.read_csv(nomearq, sep='\t')
#    
#    dicc = precoDolarBrlVenda
#
#    data = '2021-11-14' 
#    if data in dicc:
#        print(data, dicc[data])
#    
#    else:
#        #(regs.iloc[i]['Data'], '%d/%m/%Y').strftime('%Y-%m-%d')
#        dataini = datetime.datetime.strptime(data, '%Y-%m-%d')
#        for diasAntes in range(1,10):
#            dbusca = dataini-datetime.timedelta(days=diasAntes)
#            dbuscast = dbusca.strftime('%Y-%m-%d')
#            if dbuscast in dicc:
#                print(data, dbuscast, dicc[dbuscast])
#                break
    
        
        