# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 15:33:52 2021

@author: mmico
"""
import Carteira


# --------------------------------------------------    
def carregaTransacoesQuantidade(carteira, registros):
    ''' carrega apenas as quantidades de moedas, sem computar o valor médio
        carteira: objeto do tipo Carteira
        registros = [operacao], ordenado por data ('idop')
        

        operacao = {'idop': unix time da transação
            'UTC_Time': 2021-07-31 01:00:00  # datetime
            'Operation_name': 'Sell'   
            'Operation_type': 'sell' #sell, buy, deposit, withdraw, fee
            'Coin': 'BTC'
            'Change':0.01  # value
            'Remark':''
           }
    
    '''
    
    grupoop = []
    idop = None
    rett = []
    
    fop = open('../op_estado_quant_%s.txt'%carteira.local, 'wt')
    for s in registros:
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
            rett.append(ret)

    fop.close()    
    
    return rett


# --------------------------------------------------    
def carregaTransacoes(carteira, registros):
    ''' carteira: objeto do tipo Carteira
        registros = [operacao], ordenado por data ('idop')
        

        operacao = {'idop': unix time da transação
            'UTC_Time': 2021-07-31 01:00:00  # datetime
            'Operation_name': 'Sell'   
            'Operation_type': 'sell' #sell, buy, deposit, withdraw, fee
            'Coin': 'BTC'
            'Change':0.01  # value
            'Remark':''
           }
    
    '''
    
    grupoop = []
    idop = None
    
    fop = open('op_estado_quant_%s.txt'%carteira.local, 'wt')
    for s in registros:
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

    fop.close()    