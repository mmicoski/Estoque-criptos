# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 11:14:01 2021

@author: mmico

Gera uma lista com formato comum das operações da Binance
"""


import pandas as pd
import os
import numpy as np
import re
import copy
import datetime
import time


class LeOperacoesBinance:
    def __init__(self):
        ''' o formato sera o do TransactionHistory 
            cada operacao será um dicionárioi do tipo
            self.operacoes = [operacao1, operacao2, ...]
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
        
        try:
            self.moedas_conhecidas = eval(open('lista_moedas2.txt').read())
        except:
            self.moedas_conhecidas = ['BRL','BTC','ETH','AAVE','LINK','TUSD','USDT','AXS']
            
            
        self.set_mcon = set(self.moedas_conhecidas)
        self.moedas_conhecidas = sorted(list(self.set_mcon), key = lambda x:len(x), reverse=True)
        
        
       
    # -------------------------------------
    def separaMoedas(self, par):
        original = par
        for moeda in self.moedas_conhecidas:
            if re.search('^'+moeda, par):
                isep = len(moeda)
                par = par[:isep]+'|'+par[isep:]
                break
            
            elif re.search(moeda+'$', par):
                isep = len(moeda)
                par = par[:-isep]+'|'+par[-isep:]
                break

        
        par = par.replace('||','|')
            
        par = par.split('|')
        
        if 'T' in par:
            print("ERRO", par)
        
        con = [p in self.set_mcon for p in par]
        if False in con:
            self.set_mcon = self.set_mcon.union(par)
            self.moedas_conhecidas = sorted(list(self.set_mcon), key = lambda x:len(x), reverse=True) 
        
        return par
        
    # -------------------------------------
    def converteFormato_1(self, regs):
        
        data = {}
        data['Date(UTC)'] = regs['Date(UTC)'].tolist()
        data['Market'] = regs['Pair'].tolist()
        data['Type'] = regs['Side'].tolist()
        data['Price'] = regs['Price'].tolist()
        data['Amount'] = regs['Executed'].replace('[A-Z,]', '', regex=True).astype(np.float32).tolist()
        data['Total'] = regs['Amount'].replace('[A-Z,]', '', regex=True).astype(np.float32).tolist()
        
        fee = []
        feecoin = []
        for i in range(len(regs)):
            dad = regs.iloc[i]['Fee']
            ds = re.search('[0-9][A-Z]', dad)
            div =  sum(ds.span())//2
            fee.append(float(dad[:div]))
            feecoin.append(dad[div:])
            
            
        
        data['Fee'] = fee
        data['Fee Coin'] = feecoin
        
        regs2 = pd.DataFrame(data)
        
        return regs2
        


    # -------------------------------------
    def leArquivoDepositosTrades(self, nome):
        ret = ["OK",""]
        cabecalho_esperado = ['Date(UTC)', 'Market', 'Type', 'Price', 'Amount', 'Total', 'Fee', 'Fee Coin']
        
        
        opexistentes = set([op['idop'] for op in self.operacoes])
        
        if 'xlsx' in nome:
            pdregs = pd.read_excel(nome)
        elif 'csv' in nome:
            pdregs = pd.read_csv(nome)
        else:
            ret = ["NOK","formato desconhecido"]
            return ret

        if 'Pair' in pdregs.columns:
            print("convertendo 1", a)

            pdregs = self.converteFormato_1(pdregs)

            
        cabecalho = pdregs.columns.tolist()
        
        nenc = [a for a in cabecalho_esperado if a not in cabecalho]
        if len(nenc) > 0:
            ret = ["NOK","cabecalho diferente do esperado"]
            return ret
            
        for i in range(len(pdregs)):
            reg = pdregs.iloc[i]
            if type(reg['Date(UTC)']) == str:
                dth = datetime.datetime.strptime(reg['Date(UTC)'], '%Y-%m-%d %H:%M:%S')
                dth = pd.to_datetime(dth).tz_localize('UTC')
                
            else:
                dth = pd.to_datetime(reg['Date(UTC)'],unit='s').tz_localize('UTC')
                
            operacao = {'origem':nome,
                        'idop': time.mktime(dth.timetuple()),
                        'UTC_Time': dth,
                        'Operation_name':reg['Type'],
                        'Remark':'',
                        }
            
            
            if operacao['idop'] in opexistentes:
                # nao deveria repetir de um arquivo para outro
                ret = ["NOK","idop duplicado entre arquivos %s"%str(reg)]
                return ret
            
            if reg['Type'] == 'DEPOSIT':
                operacao['Operation_type'] = 'deposit'
                operacao['Coin'] = reg['Market']
                operacao['Change'] = reg['Amount']
                self.operacoes.append(operacao)
                
                    
            elif reg['Type'] == 'WITHDRAW':
                operacao['Operation_type'] = 'withdraw'
                operacao['Coin'] = reg['Market']
                operacao['Change'] = -abs(reg['Amount'])
                self.operacoes.append(operacao)

            elif reg['Type'] == 'BUY':
                moedas = self.separaMoedas(reg['Market'])
                if len(moedas) != 2:
                    ret = ["NOK","compra sem 2 moedas %s"%str(reg)]
                    return ret
                    
                operacao['Operation_type'] = 'buy'
                operacao['Coin'] = moedas[0]
                operacao['Change'] = reg['Amount']
                self.operacoes.append(operacao)

                operacao = copy.deepcopy(operacao)
                operacao['Operation_type'] = 'buy'
                operacao['Coin'] = moedas[1]
                operacao['Change'] = -abs(reg['Total'])
                self.operacoes.append(operacao)
                
            elif reg['Type'] == 'SELL':
                moedas = self.separaMoedas(reg['Market'])
                if len(moedas) != 2:
                    ret = ["NOK","compra sem 2 moedas %s"%str(reg)]
                    return ret
                    
                operacao['Operation_type'] = 'sell'
                operacao['Coin'] = moedas[0]
                operacao['Change'] = -abs(reg['Amount'])
                self.operacoes.append(operacao)

                operacao = copy.deepcopy(operacao)
                operacao['Operation_type'] = 'sell'
                operacao['Coin'] = moedas[1]
                operacao['Change'] = reg['Total']
                self.operacoes.append(operacao)
                
            else:
                ret = ["NOK","operacao desconhecida %s"%str(reg)]
                
                
            if not pd.isna(reg['Fee']) and not pd.isna(reg['Fee Coin']):
                operacao = copy.deepcopy(operacao)
                operacao['Operation_type'] = 'fee'
                operacao['Coin'] = reg['Fee Coin']
                operacao['Change'] = -abs(reg['Fee'])
                self.operacoes.append(operacao)
                
                
        
        return ret
  
    # -------------------------------------
    def leArquivoTransactions(self, nome):
        ret = ["OK",""]
        cabecalho_esperado = ['UTC_Time', 'Operation', 'Coin', 'Change', 'Remark']
        
        
        opexistentes = set([op['idop'] for op in self.operacoes])
        
        if 'xlsx' in nome:
            pdregs = pd.read_excel(nome)
        elif 'csv' in nome:
            pdregs = pd.read_csv(nome)
        else:
            ret = ["NOK","formato desconhecido"]
            return ret

#        if 'Pair' in pdregs.columns:
#            print("convertendo 1", a)
#
#            pdregs = self.converteFormato_1(pdregs)

            
        cabecalho = pdregs.columns.tolist()
        
        nenc = [a for a in cabecalho_esperado if a not in cabecalho]
        if len(nenc) > 0:
            ret = ["NOK","cabecalho diferente do esperado"]
            return ret
            
        for i in range(len(pdregs)):
            reg = pdregs.iloc[i]

    
            if reg['Operation'] in ['Fee', 'Sell', 'Buy', 'Withdraw', 'Deposit', 
                  'POS savings redemption', 'POS savings purchase']:
                # está pegando essas operações dos outros arquivos
                continue
            
            if reg['Change'] < 0:
                # está pegando essas operações dos outros arquivos
                continue
            
            dth = pd.to_datetime(reg['UTC_Time'],unit='s').tz_localize('UTC')
                
            operacao = {'origem':nome,
                        'idop': time.mktime(dth.timetuple()),
                        'UTC_Time': dth,
                        'Operation_name':reg['Operation'],
                        'Remark':reg['Remark'],
                        }
            
            
            
            if 0: #operacao['idop'] in opexistentes:
                # nao deveria repetir de um arquivo para outro
                ret = ["NOK","idop duplicado entre arquivos %s"%str(reg)]
                return ret
            
                        

            operacao['Operation_type'] = 'deposit'
            operacao['Coin'] = reg['Coin']
            operacao['Change'] = reg['Change']
            
            
            self.operacoes.append(operacao)
            
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
        
        open('lista_moedas.txt','wt').write(str(list(self.moedas_conhecidas)))
        
        return sop
        


# ==================================
if __name__ == '__main__':  



    leb = LeOperacoesBinance()


    # lê arquivos
    dirin = '../Binance/historico'
    
    arqs = [a for a in os.listdir(dirin) if 'xlsx' in a and 'lock' not in a and 'Transaction' not in a ]
    
    for a in arqs:
        ret = leb.leArquivoDepositosTrades(dirin+'/'+a)
        print(a, ret)
        if ret[0] != 'OK':
            print("FALHA", ret)
            break

        
    arqs = [a for a in os.listdir(dirin) if 'xlsx' in a and 'lock' not in a and 'Transaction' in a]
    
    for a in arqs:
        ret = leb.leArquivoTransactions(dirin+'/'+a)
        print(a, ret)
        if ret[0] != 'OK':
            print("FALHA", ret)
            break



    sop = leb.salva_registros('../regs_binance.tsv')

    # monta carteira
    import Carteira
    import CarregaTransacoes
    
    cart_bin = Carteira.Carteira('Binance',{})

    CarregaTransacoes.carregaTransacoesQuantidade(cart_bin, sop)
    cart_bin.relmoedas2()
    

    if 1:

        def  carrega_grupo(carteira, grupoop):
            qtmoeda = float(s['Change'])
            if qtmoeda >= 0:
                ret = carteira.deposita(s['Coin'], qtmoeda, 0)
        
            else:
                ret = carteira.retira(s['Coin'], abs(qtmoeda))
                
            
            fop.write(str(s)+'\n')
            for m in sorted(carteira.moedas):
                fop.write("  %s: %s\n"%(m, carteira.moedas[m]))
            
            if ret[0] != "OK":
                print(s, ret)


        cart_binval = Carteira.Carteira('BinanceRS',{})

        registros = sop
        carteira = cart_binval

        grupoop = []
        idant = None
        
        fop = open('../op_estado_total_%s.txt'%cart_binval.local, 'wt')
        for s in registros:
            idop = s['idop']
            if idop != idant:
                if idant is not None:
                    carrega_grupo(grupoop)
                
                
                idant = idop
                grupoop = []
            
            grupoop.append(s)
                
            
            
    
        fop.close()    