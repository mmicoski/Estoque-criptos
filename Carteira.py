# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 16:41:12 2021

@author: mmico
"""


class Carteira:
    ''' Guarda os valores da carteira 
        Guarda o nome, a quantidade e o preço de compra
        self.moedas = {'NOME':{'qt':10, 'totalR$':20}}
    '''
    
    def __init__(self, local, val_inicial=None):
        ''' inicia carteira 
            local: 'Binance', 'BitcoinTrade', etc    
            valor_inicial: dicionario similar a self.moedas
        '''
        self.log = False
        self.local = local
        
        if val_inicial is not None:
            self.moedas = val_inicial
            
        else:
            self.moedas = {
              'BTC':{'qt':0, 'totalR$':0},
              'ETH':{'qt':0, 'totalR$':0},
              'BRL':{'qt':0, 'totalR$':0}}
        

    # --------------------------------------------
    def deposita(self, nome, quantidade, valorRS):
        ''' adiciona uma quantidade de moeda associada a um valor em R$ 
            retorna mensagem com status da operação
        '''
        if self.log: print("deposita(nome=%s, quantidade=%f, valorRS=%.2f)"%(nome, quantidade, valorRS))
        ret = ["OK",""]
        if quantidade < 0 or valorRS < 0:
            ret = ["NOK", "deposito negativo"]
            if self.log: print("deposita() AVISO: %s"%ret[1], [nome, quantidade, valorRS])
    

        if nome not in self.moedas:
            self.moedas[nome] = {'qt':0, 'totalR$':0}
            if self.log: print("deposita() AVISO: inserindo nova moeda")
            
            
        
        self.moedas[nome]['qt'] += quantidade
        self.moedas[nome]['totalR$'] += valorRS
                
        return ret

    # --------------------------------------------
    def retira(self, nome, quantidade):
        ''' retira uma quantidade de moeda. O valor em R$ é calculado proporcionalmente 
            retorna mensagem com valor R$ da retirada e status da operação
        '''
        if self.log: print("retira(nome=%s, quantidade=%f)"%(nome, quantidade))
        ret = ["OK","", 0.0]
        if quantidade < 0:
            ret = ["NOK", "retirada negativa", 0.0]
            if self.log: print("retira() AVISO: %s"%ret[2], [nome, quantidade])
            
   
        if nome in self.moedas: 
            if quantidade > self.moedas[nome]['qt']:
                ret = ["NOK", "retirada saldo insuficiente", 0.0, self.moedas[nome]['qt']]
                if self.log: print("retira() AVISO: %s"%ret[2], [nome, quantidade])
        else:
            ret = ["NOK", "retirada sem moeda", 0.0]
            self.moedas[nome] = {'qt':0, 'totalR$':0}
            if self.log: print("retira() AVISO: %s"%ret[2], [nome, quantidade])
            
        
        qtestoque = self.moedas[nome]['qt']
        
        delta_valRS = 0.0
        
        if qtestoque != 0:
            delta_valRS = quantidade/qtestoque*self.moedas[nome]['totalR$']
            
        ret[2] = delta_valRS
        
        self.moedas[nome]['qt'] -= quantidade
        self.moedas[nome]['totalR$'] -= delta_valRS
                
        return ret
    
    # --------------------------------------------
    def relmoedas(self):
        print("=====================")
        print("Estoque de [%s]"%self.local)
        for m in sorted(self.moedas.keys()):
            print(m, self.moedas[m])
        print("=====================")
    
    
    # --------------------------------------------
    def relmoedas2(self):
        ''' ordena pelo nome da moeda '''
        print("=====================")
        print("Estoque de [%s]"%self.local)
        print("NOME ESTOQUE R$COMPRA")
        for m in sorted(self.moedas.keys()):
            print("%s %f %f"%(m, self.moedas[m]['qt'], self.moedas[m]['totalR$']))
        print("=====================")
    
    
    # --------------------------------------------
    def relmoedas_ordenado(self, campo_ord, updown):
        ''' ordena pelo campo_ord, sentido dado por updown
            campo_ord: 'nome', 'estoque','' 
            updown:  'up', 'down'
        '''
        print("=====================")
        print("Estoque de [%s]"%self.local)
        print("NOME ESTOQUE R$COMPRA")
        estoque = [[m, self.moedas[m]['qt'], self.moedas[m]['totalR$']] for m in self.moedas ]
        
        if campo_ord == 'R$':
            estoque = sorted(estoque, key=lambda x:x[2], reverse=True if updown=='down' else False)
            
        elif campo_ord == 'nome':
            estoque = sorted(estoque, key=lambda x:x[0], reverse=True if updown=='down' else False)
            
        for m in estoque:
            print("%s %f %f"%(m[0], m[1], m[2]))
        print("=====================")
        
        
# =============================
def testaCarteira():
    resultok = True
    msgs = []
    
    carteira = Carteira("teste", {})
    carteira.log = False
    
    ret = carteira.deposita('ABC', 10.0, 100.0)
    if ret[0] != 'OK':
        msgs.append("deposito retornou erro")
        print("testaCarteira() %s"%msgs[-1])
        resultok = False

    if abs(carteira.moedas['ABC']['qt'] - 10.0) > 1e-5:
        msgs.append("deposito errou no cálculo da quantidade")
        print("testaCarteira() %s"%msgs[-1])
        resultok = False

    if abs(carteira.moedas['ABC']['totalR$'] - 100.0) > 1e-5:
        msgs.append("deposito errou no cálculo do totalR$")
        print("testaCarteira() %s"%msgs[-1])
        resultok = False

    
    ret = carteira.deposita('ABC', 5.0, 200.0)
    if ret[0] != 'OK':
        msgs.append("deposito retornou erro")
        print("testaCarteira() %s"%msgs[-1])
        resultok = False

    if abs(carteira.moedas['ABC']['qt'] - 15.0) > 1e-5:
        msgs.append("deposito errou no cálculo da quantidade")
        print("testaCarteira() %s"%msgs[-1])
        resultok = False

    if abs(carteira.moedas['ABC']['totalR$'] - 300.0) > 1e-5:
        msgs.append("deposito errou no cálculo do totalR$")
        print("testaCarteira() %s"%msgs[-1])
        resultok = False


    ret = carteira.retira('ABC', 1)
    if abs(ret[2] - 20.0) > 1e-5:
        msgs.append("retirada errou cálculo de delta_totalR$")
        print("testaCarteira() %s"%msgs[-1])
        resultok = False

    if ret[0] != 'OK':
        msgs.append("retirada retornou erro")
        print("testaCarteira() %s"%msgs[-1])
        resultok = False

    if abs(carteira.moedas['ABC']['qt'] - 14.0) > 1e-5:
        msgs.append("retirada errou no cálculo da quantidade")
        print("testaCarteira() %s"%msgs[-1])
        resultok = False

    if abs(carteira.moedas['ABC']['totalR$'] - 280.0) > 1e-5:
        msgs.append("retirada errou no cálculo do totalR$")
        print("testaCarteira() %s"%msgs[-1])
        resultok = False


    ret = carteira.retira('XYZ', 1)
    if ret[0] != 'NOK':
        msgs.append("retirada não apontou erro sem saldo")
        print("testaCarteira() %s"%msgs[-1])
        resultok = False
    

    ret = carteira.retira('ABC', 100)
    if ret[0] != 'NOK':
        msgs.append("retirada não apontou saldo insuficiente")
        print("testaCarteira() %s"%msgs[-1])
        resultok = False


    return resultok,msgs
    
# ==================================
if __name__ == '__main__':        
    
    ret = testaCarteira()
    print("\n=================\n= Autoteste: %s"%("OK" if ret[0] else "NOK"))
    if not ret[0]:
        for msg in ret[1]:
            print("= *", msg)
    print("=================")

    carteira = Carteira("teste", {})
    carteira.log = True
    
    ret = carteira.deposita('ABC', 10.0, 100.0)
    print(ret)
    carteira.relmoedas()
    ret = carteira.deposita('ABC', 5.0, 200.0)
    print(ret)
    carteira.relmoedas()

    ret = carteira.retira('ABC', 1)
    print(ret)
    carteira.relmoedas()


    ret = carteira.retira('XYZ', 1)
    print(ret)
    carteira.relmoedas()
    
    ret = carteira.retira('ABC', 100)
    print(ret)
    carteira.relmoedas()
    
    ret = carteira.deposita('CDE', -100, 100)
    print(ret)
    carteira.relmoedas()
    
    
    ret = carteira.deposita('CDE', 100, -100)
    print(ret)
    carteira.relmoedas()
    