# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 15:33:52 2021

@author: mmico
Carrega transações na carteira, usando o princípio de que apenas a troca por BRL 
é venda, isto é, uma  permuta de cripto por cripto não altera o valor R$ de 
compra.

"""

mesames = {}  # {anomes: {'opRS':operacoes, 'vendaRS':val venda, 'lucroRS':lucro venda}}
anomes = None


RS_declara_operacoes = 30000
RS_imposto_venda = 35000
        

# -----------------------------------------
def  carrega_grupo(carteira, grupoop):
    global mesames
    global anomes
    
    anomes = grupoop[0]['UTC_Time'].strftime("%Y%m")
    valsmes = mesames.get(anomes,{'opRS':0.0, 'vendaRS':0.0, 'lucroRS':0.0})
    
    ret = ["OK",""]
    resumo  = {}
    operacoes = {}
    opnames = {}
    valRS = {}  # valor R$ anotado no campo Remark
    for op in grupoop:
        resumo[op['Coin']] = resumo.get(op['Coin'],0) + op['Change']
        operacoes[op['Operation_type']] = 1
        opnames[op['Operation_name']] = 1
        if 'ValRS=' in op['Remark']:
            valbrl = float(op['Remark'].split('=')[1])
            valRS[op['Coin']] = valRS.get(op['Coin'],0) + valbrl
            
        
    ops = '.'.join(sorted(operacoes.keys()))
    
    if ops == 'deposit':
        
        for moeda in resumo:
            change = resumo[moeda]
            opname = [ k for k in opnames][0].lower()
            rewardnames = ['staking', 'commission', 'interest']
            if len(opnames) == 1 and len([1 for r in rewardnames if r in opname])>0:
                # staking tem custo zero
                retd = carteira.deposita(moeda, change, 0.0)
                if retd[0] != "OK":
                    ret = ["NOK", "erro em deposito: %s"%str(retd)]

            elif moeda == 'BRL' and change > 0:
                retd = carteira.deposita(moeda, change, change)
                valsmes['opRS'] += abs(change)
                
                if retd[0] != "OK":
                    ret = ["NOK", "erro em deposito: %s"%str(retd)]
            
            elif moeda != 'BRL' and moeda in valRS:
                retd = carteira.deposita(moeda, change, valRS[moeda])
                valsmes['opRS'] += abs(valRS[moeda])
                
                if retd[0] != "OK":
                    ret = ["NOK", "erro em deposito: %s"%str(retd)]
                
            
            else:
                ret = ["NOK","deposito desconhecido: %s"%str(grupoop)]
                print(ret)
                
    elif ops == 'withdraw' or ops == 'fee.withdraw':
        for moeda in resumo:
            change = resumo[moeda]
            retw = carteira.retira(moeda, abs(change))
            valsmes['opRS'] += abs(retw[2])
            
            if retw[0] != "OK":
                ret = ["NOK", "erro em retirada: %s"%str(retw)]
                

    elif ops == 'buy' or ops == 'buy.fee' \
         or ops == 'sell' or ops == 'fee.sell':
        
        moeda_retira = [[m, resumo[m]] for m in resumo if resumo[m] < 0]
        moeda_deposita = [[m, resumo[m]] for m in resumo if resumo[m] > 0]
        valsop = {'BRLfatura':0.0, 'BRLcusto':0.0}
        
        if moeda_deposita[0][0] == 'BRL':
            print("venda por BRL")
        
        if len(moeda_retira) >= 1 and len(moeda_deposita) == 1:
            # dá uma ou mais moedas para adquirir uma moeda
            # --- LADO DA VENDA (MOEDAS ENTREGUES) -----------
            valorRSvenda = 0.0
            valorRScusto = 0.0

            for mr in moeda_retira:
                retr = carteira.retira(mr[0], abs(mr[1]))
                if retr[0]!= "OK":
                    ret = ["NOK", "erro em buy.sell.retirada: %s"%str(retr)]
                
                valorRSvenda += abs(retr[2])
                valorRScusto += abs(retr[2])
            # ------------------
            
            # ------ LADO DA COMPRA (MOEDA RECEBIDA) ---------------
            if moeda_deposita[0][0] == 'BRL':
                # venda por R$
                valorRSvenda = moeda_deposita[0][1]
                valsop['BRLfatura'] +=  abs(valorRSvenda)

                
            valsop['BRLcusto'] += valorRScusto
            valsmes['opRS'] += abs(valorRSvenda)
                
            retd = carteira.deposita(moeda_deposita[0][0], moeda_deposita[0][1], valorRSvenda)


            if valsop['BRLfatura'] > 0:
                # se recebeu BRL, eh venda
                lucro = valsop['BRLfatura'] - valsop['BRLcusto']
                valsmes['vendaRS'] += valsop['BRLfatura']
                if lucro > 0:
                    valsmes['lucroRS'] += lucro

            if retd[0]!= "OK":
                ret = ["NOK", "erro em buy.sell.deposito: %s"%str(retd)]


            
        else:
            ret = ["NOK", "ERRO em buy.sell %s"%str(grupoop)]
            print(ret)
                
    else:
        ret = ["NOK","operacao desconhecida: %s"%str(grupoop)]
        print("ERRO:", ops)
        
        
    mesames[anomes] = valsmes
        
    return ret

# --------------------------------------------------    
def carregaTransacoes(carteira, registros):
    ''' carrega as quantidades de moedas, computando o valor médio
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
    grupoop = []
    idant = None
    
    fop = open('../op_estado_total_%s.txt'%carteira.local, 'wt')
    for s in registros:
        idop = s['idop']
        if idop != idant:
            if idant is not None:
                
                ret = carrega_grupo(carteira, grupoop)
                if ret[0] != "OK":
                    print(s, ret)
                    rett.append(ret)
                    
                fop.write("============================\n")
                for op in grupoop:
                    fop.write(str(op)+'\n')
                
                fop.write(anomes+' '+str(mesames[anomes])+'\n')
                    
                for m in sorted(carteira.moedas.keys()):
                    fop.write("  %s %s"%(m, str(carteira.moedas[m]))+'\n')
            
            # ---- if idant is not None:
            
            idant = idop
            grupoop = []
        
        # ---------if idop != idant:
        
        grupoop.append(s)
            
        
    # --- for s in registros:  
    
    # ultimo registro, se houver
    if len(grupoop) > 0:
        ret = carrega_grupo(carteira, grupoop)
        if ret[0] != "OK":
            print(s, ret)
            rett.append(ret)
            
        fop.write("============================\n")
        for op in grupoop:
            fop.write(str(op)+'\n')
            
        fop.write(anomes+' '+str(mesames[anomes])+'\n')
            
        for m in sorted(carteira.moedas.keys()):
            fop.write("  %s %s"%(m, str(carteira.moedas[m]))+'\n')
                    

    fop.close()  
        
    return rett, mesames


# --------------------------------------------------    
def relatorioPorMes():
    meses = sorted(mesames.keys())
    print("AAAAMM\tdec\timp\toperacoes\tvendas\tlucro" )
    for mes in meses:
        vals = mesames[mes]
        declara = "SIM" if vals['opRS'] > RS_declara_operacoes else "nao"
        imposto = "SIM" if vals['vendaRS'] > RS_imposto_venda else "nao"
        print("%s\t%s\t%s\t%5.2f\t%5.2f\t%5.2f"%(mes, declara, imposto, vals['opRS'], vals['vendaRS'], vals['lucroRS']))
    
    
# --------------------------------------------------    
if __name__ == "__main__":
    # testes
    import Carteira
    import pandas as pd 
    
    ok = True
    
    cartTeste = Carteira.Carteira('TesteRS',{})
    mesames = {} 
    
    # um registro
    regs = [{'origem': 'a1', 
     'idop': 1577145444.0, 
     'UTC_Time': pd.Timestamp('2019-12-23 20:57:24+0000', tz='UTC'), 
     'Operation_name': 'DEPOSIT', 
     'Remark': '', 
     'Operation_type': 'deposit', 
     'Coin': 'BRL', 'Change': 1000.0}]
            
    rett, mesames = carregaTransacoes(cartTeste, regs)
    if  cartTeste.moedas != {'BRL': {'qt': 1000.0, 'totalR$': 1000.0}}:
        ok = False
        print("ERRO 1.0")
        
    if mesames != {'201912': {'opRS': 1000.0, 'vendaRS': 0.0, 'lucroRS': 0.0}}:
        ok = False
        print("ERRO 1.1")
        
    print(mesames)
    cartTeste.relmoedas()
        
    