# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 15:33:52 2021

@author: mmico
"""

mesames = {}  # {anomes: {'opRS':operacoes, 'vendaRS':val venda, 'lucroRS':lucro venda}}
anomes = None


RS_declara_operacoes = 30000
RS_imposto_venda = 35000
        
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
if __name__ == "__main__":
    # testes
    import Carteira
    import pandas as pd 
    
    ok = True
    
    cartTeste = Carteira.Carteira('Teste',{})
    
    # um registro
    regs = [{'origem': 'a1', 
     'idop': 1577145444.0, 
     'UTC_Time': pd.Timestamp('2019-12-23 20:57:24+0000', tz='UTC'), 
     'Operation_name': 'DEPOSIT', 
     'Remark': '', 
     'Operation_type': 'deposit', 
     'Coin': 'BRL', 'Change': 1000.0}]
            
    rett = carregaTransacoesQuantidade(cartTeste, regs)
    print(rett)    
    cartTeste.relmoedas()