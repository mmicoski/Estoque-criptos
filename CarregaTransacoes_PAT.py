# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 15:33:52 2021

@author: mmico

Carrega transações na carteira, usando o princípio de que permuta=venda, isto é,
uma permuta de cripto atualiza o valor em R$ de compra da cripto comprada de acordo com
o valor de mercado da cripto vendida no momento da troca.
"""

import HistoricoCripto
import Carteira


class CarregaTransacoes_PAT:
    ''' Carrega transações na carteira, usando o princípio de que permuta=venda, isto é,
    uma permuta de cripto atualiza o valor em R$ de compra da cripto comprada de acordo com
    o valor de mercado da cripto vendida no momento da troca.
    '''
    def __init__(self, nomeCarteira, histcotacoes=None):
        
        if histcotacoes is not None:
            self.hc = histcotacoes
            
        else:
            self.hc = HistoricoCripto.HistoricoCotacao()
            self.hc.leHistoricoDolar('../cotacoes/USDBRL_BCB.tsv')
        
        self.carteira = Carteira.Carteira(nomeCarteira,{})
        
        self.mesames = {}  # {anomes: {'opRS':operacoes, 'vendaRS':val venda, 'lucroRS':lucro venda}}
        self.anomes = None


        self.RS_declara_operacoes = 30000
        self.RS_imposto_venda = 35000
        
    
    # -----------------------------------------
    def carrega_grupo(self, grupoop):
        
        self.anomes = grupoop[0]['UTC_Time'].strftime("%Y%m")
        valsmes = self.mesames.get(self.anomes,{'opRS':0.0, 'vendaRS':0.0, 'lucroRS':0.0})
        
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
                    retd = self.carteira.deposita(moeda, change, 0.0)
                    if retd[0] != "OK":
                        ret = ["NOK", "erro em deposito: %s"%str(retd)]
    
                elif moeda == 'BRL' and change > 0:
                    retd = self.carteira.deposita(moeda, change, change)
                    valsmes['opRS'] += abs(change)
                    
                    if retd[0] != "OK":
                        ret = ["NOK", "erro em deposito: %s"%str(retd)]
                
                elif moeda != 'BRL' and moeda in valRS:
                    retd = self.carteira.deposita(moeda, change, valRS[moeda])
                    valsmes['opRS'] += abs(valRS[moeda])
                    
                    if retd[0] != "OK":
                        ret = ["NOK", "erro em deposito: %s"%str(retd)]
                    
                
                else:
                    ret = ["NOK","deposito desconhecido: %s"%str(grupoop)]
                    print(ret)
                    
        elif ops == 'withdraw' or ops == 'fee.withdraw':
            for moeda in resumo:
                change = resumo[moeda]
                retw = self.carteira.retira(moeda, abs(change))
                valsmes['opRS'] += abs(retw[2])
                
                if retw[0] != "OK":
                    ret = ["NOK", "erro em retirada: %s"%str(retw)]
                    
    
        elif ops == 'buy' or ops == 'buy.fee' \
             or ops == 'sell' or ops == 'fee.sell':
            
            moeda_retira = [[m, resumo[m]] for m in resumo if resumo[m] < 0]
            moeda_deposita = [[m, resumo[m]] for m in resumo if resumo[m] > 0]
            valsop = {'BRLfatura':0.0, 'BRLcusto':0.0}
            
            datast = grupoop[0]['UTC_Time'].strftime("%Y-%m-%d")
            
            if moeda_deposita[0][0] == 'BRL':
                print("venda por BRL")
            
            if len(moeda_retira) >= 1 and len(moeda_deposita) == 1:
                # dá uma ou mais moedas para adquirir uma moeda
                # --- LADO DA VENDA (MOEDAS ENTREGUES) -----------
                valorRSvenda = 0.0
                valorRScusto = 0.0
                for mr in moeda_retira:
                    retr = self.carteira.retira(mr[0], abs(mr[1]))
                    valorRScusto += abs(retr[2])
                    
                    if retr[0]!= "OK":
                        ret = ["NOK", "erro em buy.sell.retirada: %s"%str(retr)]
                    
                    if self.hc is not None:
                        # calcula valor R$ pela cotacao da moeda usada como pagamento
                        if mr[0] == 'BRL':
                            valCRS = abs(mr[1])
                            
                        else:
                            valUSD = self.hc.consultaCripto(mr[0], datast) * abs(mr[1])
                            USDBRL = self.hc.consultaDolar(datast, compra=True)
                            valCRS = valUSD * USDBRL
                            
                        
                        valorRSvenda += valCRS
                        
                    else:
                        # sem cotacao: usa valor de compra da moeda entregue
                        valorRSvenda += retr[2]
                        
                # ------------------------------
                
                # ------ LADO DA COMPRA (MOEDA RECEBIDA) ---------------
                if moeda_deposita[0][0] == 'BRL':
                    # venda por R$
                    valorRSvenda = moeda_deposita[0][1]
                
                retd = self.carteira.deposita(moeda_deposita[0][0], moeda_deposita[0][1], valorRSvenda)
                    

                valsop['BRLfatura'] +=  abs(valorRSvenda)
                valsop['BRLcusto'] += valorRScusto
                valsmes['opRS'] += abs(valorRSvenda)

                ehvenda = False
                
                if self.hc is not None:
                    # cenario com cotacoes (PAT)
                    if 'BRL' not in [m[0] for m in moeda_retira]:
                        # se não entregou BRL, eh venda
                        ehvenda = True
                        
                else:
                    # cenario sem cotacoes (so troca por BRL eh venda)
                    if 'BRL' in [m[0] for m in moeda_deposita]:
                        ehvenda = True
                    
                if ehvenda:
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
            
            
        self.mesames[self.anomes] = valsmes
            
        return ret
    
    # --------------------------------------------------    
    def carregaTransacoes(self, registros):
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
        
        fop = open('../op_estado_total_%s.txt'%self.carteira.local, 'wt')
        for s in registros:
            idop = s['idop']
            if idop != idant:
                if idant is not None:
                    
                    ret = self.carrega_grupo(grupoop)
                    if ret[0] != "OK":
                        print(s, ret)
                        rett.append(ret)
                        
                    fop.write("============================\n")
                    for op in grupoop:
                        fop.write(str(op)+'\n')
                    
                    fop.write(self.anomes+' '+str(self.mesames[self.anomes])+'\n')
                        
                    for m in sorted(self.carteira.moedas.keys()):
                        fop.write("  %s %s"%(m, str(self.carteira.moedas[m]))+'\n')
                
                # ---- if idant is not None:
                
                idant = idop
                grupoop = []
            
            # ---------if idop != idant:
            
            grupoop.append(s)
                
            
        # --- for s in registros:  
        
        # ultimo registro, se houver
        if len(grupoop) > 0:
            ret = self.carrega_grupo(grupoop)
            if ret[0] != "OK":
                print(s, ret)
                rett.append(ret)
                
            fop.write("============================\n")
            for op in grupoop:
                fop.write(str(op)+'\n')
                
            fop.write(self.anomes+' '+str(self.mesames[self.anomes])+'\n')
                
            for m in sorted(self.carteira.moedas.keys()):
                fop.write("  %s %s"%(m, str(self.carteira.moedas[m]))+'\n')
                        
    
        fop.close()  
            
        return rett, self.mesames
    
    
    # --------------------------------------------------    
    def relatorioPorMes(self):
        meses = sorted(self.mesames.keys())
        print("AAAAMM\tdec\timp\toperacoes\tvendas\tlucro" )
        for mes in meses:
            vals = self.mesames[mes]
            declara = "SIM" if vals['opRS'] > self.RS_declara_operacoes else "nao"
            imposto = "SIM" if vals['vendaRS'] > self.RS_imposto_venda else "nao"
            print("%s\t%s\t%s\t%5.2f\t%5.2f\t%5.2f"%(mes, declara, imposto, vals['opRS'], vals['vendaRS'], vals['lucroRS']))
        
    
# --------------------------------------------------    
if __name__ == "__main__":
    # testes
    import pandas as pd 
    import Testa_CarregaTransacoes as tct
    
    ok = True
    
    
    ccpat = CarregaTransacoes_PAT('Teste')
    
    if 0:
        # com cotacoes
        ccpat.hc.precoCriptoUsd['BTC']['2019-12-23'] = 9000
        ccpat.hc.precoDolarBrlCompra['2019-12-23'] = 2.0
        ccpat.hc.precoDolarBrlVenda['2019-12-23'] = 2.0
        
    else:
        # sem cotacoes
        ccpat.hc = None
            
    rett, mesames = ccpat.carregaTransacoes(tct.regs[:6])

    print(ccpat.mesames)
    ccpat.carteira.relmoedas()
        
    