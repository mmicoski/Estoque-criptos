# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 19:17:57 2021

@author: mmico

É necessário ter a extensão 'xlrd' do Pandas para ler o Excel.
Na máquina do Mauricio, está no ambiente "excel".
    Anaconda prompt
    activate excel
    spyder
"""

import pandas as pd
import os
import numpy as np
import re
import copy

import Carteira

fout = open('../estado_binance.txt','wt')
fop = open('../operacoes_binance.txt','wt')

fop.write("dth(utc);moeda_venda;qt_venda;moeda_compra;qt_compra;valR$;taxaR$\n")


# --------------------------------------------
def descontaTaxa(reg):
    fee = reg['Fee']
    feecoin = reg['Fee Coin']
    deltaRS = 0
    
    if feecoin in moedas:
        if not np.isnan(fee) and fee > 0:
            moedafee = moedas[feecoin]
            deltaRS = moedafee['totalR$']/moedafee['qt']*fee
            
            if np.isnan(deltaRS):
                print(reg)
            
            if moedas[feecoin]['qt'] < fee:
                print("ERRO taxa maior do que tem")
                print(reg)
                print(moedas)
            
            moedas[feecoin]['qt'] -= fee
            moedas[feecoin]['totalR$'] -= deltaRS
        
    elif fee > 0:
        print("feecoin desconhecida", feecoin, reg) 
        
    return deltaRS

# --------------------------------------------
def atualizaDthMed(moeda, regdth, regqt):
    ''' atualiza a data hora de compra como a média ponderada das datas de compra e quantidades compradas '''
    if 'dthmed_utc' not in moeda or moeda['qt'] == 0:
        moeda['dthmed_utc'] = regdth
        return
    
    dtnovo = (reg["Date(UTC)"]-moeda['dthmed_utc']).total_seconds()*regqt/(regqt+moeda['qt'])
    moeda['dthmed_utc'] = moeda['dthmed_utc'] + pd.Timedelta(seconds=dtnovo)
    
# --------------------------------------------

moedas = Carteira.Carteira('Binance', {})

vendas = []

#diret = '../historico-Binance'
diret = '../Binance/historico'

arqs = sorted([a for a in os.listdir(diret) if 'xlsx' in a.lower() and 'lock' not in a.lower()])

regstotal = None

regs = []

for a in arqs:

    regsarquivo = pd.read_excel(diret+'/'+a)
    if 'Pair' in regsarquivo.columns:
        #continue

        print("convertendo", a)
        
        data = {}
        data['Date(UTC)'] = regsarquivo['Date(UTC)'].tolist()
        data['Market'] = regsarquivo['Pair'].tolist()
        data['Type'] = regsarquivo['Side'].tolist()
        data['Price'] = regsarquivo['Price'].tolist()
        data['Amount'] = regsarquivo['Executed'].replace('[A-Z,]', '', regex=True).astype(np.float32).tolist()
        data['Total'] = regsarquivo['Amount'].replace('[A-Z,]', '', regex=True).astype(np.float32).tolist()
        
        fee = []
        feecoin = []
        for i in range(len(regsarquivo)):
            dad = regsarquivo.iloc[i]['Fee']
            ds = re.search('[0-9][A-Z]', dad)
            div =  sum(ds.span())//2
            fee.append(float(dad[:div]))
            feecoin.append(dad[div:])
            
            
        
        data['Fee'] = fee
        data['Fee Coin'] = feecoin
        
        
        
        regs2 = pd.DataFrame(data)

        print("acumulando",a, regs2['Date(UTC)'].min(),"a",regs2['Date(UTC)'].max())
        regs.append(regs2)
        
    else:           
        print("acumulando",a, regsarquivo['Date(UTC)'].min(),"a",regsarquivo['Date(UTC)'].max())
        regs.append(regsarquivo)

    # --- if 'Pair' in regsarquivo.columns:    


regstotal = pd.concat(regs)


regstotal['Fee'] = regstotal['Fee'].fillna(0.0)

regstotal['Date(UTC)'] = regstotal['Date(UTC)'].apply(lambda x:pd.Timestamp(x))

sregs = regstotal.sort_values('Date(UTC)')

regant = None

for i in range(sregs.shape[0]):
    reg = sregs.iloc[i]
    
    if regant is not None:
        igual = (reg == regant).all()
        if igual:
            print("AVISO: registro repetido: %s"%str(reg))
            
    regant = reg
        

    
    if reg['Type'] == 'DEPOSIT':
        atualizaDthMed(moedas[reg['Market']], reg["Date(UTC)"], reg['Total'])
        moedas[reg['Market']]['qt'] += reg['Total']
        moedas[reg['Market']]['totalR$'] += reg['Total']
    
    elif reg['Type'] == 'WITHDRAW':
        nome_moeda = reg['Market']
        moeda = moedas[nome_moeda]
        
        qt = reg['Total']
        
        if qt > moeda['qt']:
            print("=====================")
            print("ERRO saca mais que tem")
            print(reg)
            print(nome_moeda, moeda)
            print(moedas)
        
        deltaRS = moeda['totalR$']/moeda['qt']*qt
        
        moedas[nome_moeda]['qt'] -= reg['Total']
        moedas[nome_moeda]['totalR$'] -= deltaRS
        
        taxaRS = descontaTaxa(reg)
        
        dados_op = {"data_utc": reg['Date(UTC)'].strftime("%d/%m/%Y %H:%M:%S"),
                 "nomemoeda": nome_moeda,
                 "qtmoeda": qt,
                 "BRLoperacao": deltaRS,
                 "taxa_RS": taxaRS
                 }



    elif reg['Type'] == 'BUY' or reg['Type'] == 'SELL':
        market = reg['Market']
        for moeda in moedas:
            market = market.replace(moeda, '|%s|'%moeda)
        
        market = market.replace('||','|')
        if market[0]=='|':
            market = market[1:]
        if market[-1]=='|':
            market = market[:-1]
            
        moedas_negocio = market.split('|')

        if reg['Type'] == 'BUY':
            signvals = [1,-1]
        elif reg['Type'] == 'SELL':
            signvals = [-1,1]
        else:
            print("erro de tipo")
            quit()

        vals_moedas = [reg['Amount'], reg['Total']]

        for m in moedas_negocio:
            if m not in moedas:
                moedas[m] = {'qt':0, 'totalR$':0}
                
        indvd = signvals.index(-1)
        indcp = 1-indvd
        
        qtvd = vals_moedas[indvd]
        if qtvd > moedas[moedas_negocio[indvd]]['qt']:
            print("=====================")
            print("ERRO vende mais que tem")
            print(reg)
            print(moedas_negocio[indvd], moedas[moedas_negocio[indvd]])
            print(moedas)
            #raise ValueError("Vende mais que tem")
            

        valRS = qtvd * moedas[moedas_negocio[indvd]]['totalR$']/moedas[moedas_negocio[indvd]]['qt']
        
        if np.isnan(valRS):
            a=1

        # executa o negocio
        res_nomemoeda_vd = moedas_negocio[indvd]
        res_qtmoeda_vd = qtvd
        res_BRLoperacao = valRS
        
        res_nomemoeda_cp = moedas_negocio[indcp]
        res_qtmoeda_cp = vals_moedas[indcp]
        
        moedas_sav = None
        if res_nomemoeda_cp == 'BRL':
            # salva para calculo do imposto
            moedas_sav = copy.deepcopy(moedas)


        ## subtrai da venda        
        moedas[res_nomemoeda_vd]['qt'] -= res_qtmoeda_vd
        if res_nomemoeda_vd == 'BRL':
            moedas[res_nomemoeda_vd]['totalR$'] -= res_qtmoeda_vd
            res_BRLoperacao = res_qtmoeda_vd
        else:
            moedas[res_nomemoeda_vd]['totalR$'] -= res_BRLoperacao

        ## soma na compra
        #atualizaDthMed(moedas[res_nomemoeda_cp], moedas[res_nomemoeda_vd]['dthmed_utc'], res_qtmoeda_cp)
        atualizaDthMed(moedas[res_nomemoeda_cp], reg['Date(UTC)'], res_qtmoeda_cp)
        moedas[res_nomemoeda_cp]['qt'] += res_qtmoeda_cp
        if res_nomemoeda_cp == 'BRL':
            moedas[res_nomemoeda_cp]['totalR$'] += res_qtmoeda_cp
            res_BRLoperacao = res_qtmoeda_cp
        else:
            moedas[res_nomemoeda_cp]['totalR$'] += res_BRLoperacao
        
        ## subtrai taxa
        res_taxa_RS = descontaTaxa(reg)
        
        if moedas_negocio[indcp] == 'BRL':
            print('\n=======\nvolta real\n=======\n',reg)



        fop.write('%s;%s;%f;%s;%f;%f;%f\n'%(reg['Date(UTC)'],
                              res_nomemoeda_vd, res_qtmoeda_vd,
                              res_nomemoeda_cp, res_qtmoeda_cp,
                              res_BRLoperacao, res_taxa_RS))
            


        dados_op = {"data_utc": reg['Date(UTC)'].strftime("%d/%m/%Y %H:%M:%S"),
                 "nomemoeda_vd": res_nomemoeda_vd,
                 "qtmoeda_vd": res_qtmoeda_vd,
                 "BRLoperacao": res_BRLoperacao,
                 "nomemoeda_cp": res_nomemoeda_cp,
                 "qtmoeda_cp": res_qtmoeda_cp,
                 "taxa_RS": res_taxa_RS
                 }

        if res_nomemoeda_cp == 'BRL':
            # salva para calculo do imposto
            vendas.append([copy.deepcopy(dados_op), moedas_sav])
            
            #valcompra = dados_op['qtmoeda_vd']/moedas_sav[res_nomemoeda_vd]['qt']*moedas_sav[res_nomemoeda_vd]['totalR$']



            
        
        
    else:
        print("Erro: operação desconhecida")
        print(reg)
        
    # ------ if reg['Type'] == 'DEPOSIT':
        
        
    fout.write(str(reg.tolist())+'\n')
    for m in moedas:
        fout.write("  %s: %s\n"%(m, str(moedas[m])))

    fout.flush()
    
fout.close()
fop.close()


relmoedas2()


# operacoes de um mês
dini = pd.Timestamp('2021-05-01 00:00:00')
dfim = pd.Timestamp('2021-05-30 23:59:59')
stdth = "Date(UTC)"
smes = [sregs.iloc[i] for i in range(len(sregs)) if 
        sregs.iloc[i][stdth]>=dini and sregs.iloc[i][stdth]<=dfim]

pdmes = sregs[sregs['Date(UTC)']>=dini]
pdmes = pdmes[pdmes['Date(UTC)']<=dfim]

sregs.to_excel('sregs.xlsx')