# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 22:34:57 2021

@author: mmico

Lê extrato da Bitcointrade e gera uma lista com formato padrão
"""


import pandas as pd
import os
import numpy as np
import re
import copy
import datetime
import time



class LeOperacoesBitcointrade:
    def __init__(self):
        ''' o formato padrão sera o do TransactionHistory da Binance
            
            self.operacoes = [operacao1, operacao2, ...]
            cada operacao será um dicionárioi do tipo
            operacao = {'idop': 
                        'UTC_Time': 2021-07-31 01:00:00  # datetime
                        'Operation_name': 'Sell'   
                        'Operation_type': 'sell' #sell, buy, deposit, withdraw, fee
                        'Coin': 'BTC'
                        'Change':0.01  # value
                        'Remark':''
                       }
            
        '''
        self.operacoes = []
        
        self.moedas_conhecidas = ['BRL','BTC','ETH']
        
        self.siglas = {
                'Real':'BRL',
                'Bitcoin':'BTC',
                'Ethereum':'ETH'
                }
        
    # -------------------------------------
    def traduzCategoria(self, cat):
        if re.search("Dep.sito", cat):
            return 'deposit'
        elif "Retirada" in cat:
            return 'withdraw'
        elif "Taxa" in cat:
            return 'fee'
        elif 'Compra' in cat:
            return 'buy'
        elif 'Venda' in cat:
            return 'sell'
        else:
            return "None"
    
    # -------------------------------------
    def leExtrato(self, nome):
        ret = ["OK",""]
        cabecalho_esperado = ['Data-UTC', 'Moeda', 'Categoria', 'Valor']
        
        
        if 'xlsx' in nome:
            pdregs = pd.read_excel(nome)
        elif 'csv' in nome:
            pdregs = pd.read_csv(nome)
        else:
            ret = ["NOK","formato desconhecido"]
            return ret
        
        
        cabecalho = pdregs.columns.tolist()
        
        nenc = [a for a in cabecalho_esperado if a not in cabecalho]
        if len(nenc) > 0:
            ret = ["NOK","cabecalho diferente do esperado"]
            return ret       
        
        for i in range(len(pdregs)):
            reg = pdregs.iloc[i] 

            dth = pd.to_datetime(reg['Data-UTC'],unit='s').tz_localize('UTC')
            
            cat = reg['Categoria']
            
            tipo = self.traduzCategoria(cat)
            if tipo == "None":
                ret = ["NOK", "categoria %s desconhecida"%cat]
            
            
            moeda = self.siglas.get(reg['Moeda'], "None")
            if moeda == "None":
                ret = ["NOK", "moeda %s desconhecida"%reg['Moeda']]
            
            operacao = {'idop': time.mktime(dth.timetuple()),
                        'UTC_Time': dth,
                        'Operation_name': cat,   
                        'Operation_type': tipo, 
                        'Coin': moeda,
                        'Change': reg['Valor'],
                        'Remark':''
                       }          
            
            
            self.operacoes.append(operacao)
           
        # --- end for i in range(len(pdregs)):
           
        return ret
          
            
        
  # -----------------------------------------------
    def salva_registros(self, nomeout):
        sop =  sorted(self.operacoes, key = lambda x:x['idop'])
        
        fout= open(nomeout,'wt')
        titulos = list(sop[0].keys())
        fout.write('\t'.join(titulos) + '\n')
        for s in sop:
            fout.write('\t'.join([str(s[t]) for t in titulos])+ '\n')
            
        fout.close()
        
        
        return sop
        
    # -----------------------------------------------
    def carrega_registros(self, nomein):
        self.operacoes = []
        fin = open(nomein, 'rt')
        titulos = fin.readline().rstrip().split('\t')
        
        dads = [a.rstrip().split('\t') for a in fin.readlines()]

        for dad in dads:
            op = {t:v for t,v in zip(titulos, dad)}
            op['idop'] = np.float64(op['idop'])
            op['UTC_Time'] = pd.Timestamp(op['UTC_Time'])
            op['Change'] = np.float64(op['Change'])
            self.operacoes.append(op)
            
            
        sop =  sorted(self.operacoes, key = lambda x:x['idop'])
        
        return sop                
        
        
# ==================================
if __name__ == '__main__':  

    leb = LeOperacoesBitcointrade()

    if 1:
        #####################################
        # 1. le extrato
    
    
        # lê arquivos
        dirin = '../Bitcointrade/historico'
        
        arqs = [a for a in os.listdir(dirin) if 'xlsx' in a and 'extrato' in a and 'lock' not in a]
        
        for a in arqs:
            ret = leb.leExtrato(dirin+'/'+a)
            print(a, ret)
            if ret[0] != 'OK':
                print("FALHA", ret)
                break
            
            
        #########################
        # 2. Salva registros ordenados
        sopbt = leb.salva_registros('../regs_bitcointrade.tsv')
        
    else:
        ## carrega arquivo pronto
        sopbt = leb.carrega_registros('../regs_bitcointrade.tsv')    

    
    ###########################
    # 3. monta carteira
    import Carteira
    import CarregaTransacoes
    
    if 1:
    
        cart_bit = Carteira.Carteira('Bitcointrade',{})
    
        # carrega apenas quantidades, o que é mais fácil de verificar
        CarregaTransacoes.carregaTransacoesQuantidade(cart_bit, sopbt)
        cart_bit.relmoedas2()
        
        
    ###############
    # 3. analisa valores em R$
    # analisa registros da mesma data-hora
    if 1:
        
        cart_bitval = Carteira.Carteira('BitcointradeRS',{})
        cart_bitval.log = False

        CarregaTransacoes.carregaTransacoes(cart_bitval, sopbt)
        cart_bitval.relmoedas2()        