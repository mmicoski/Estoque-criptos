# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 12:08:49 2021

@author: mmico
"""

# testes
import Carteira
import CarregaTransacoes_PAT
import pandas as pd 


precoCriptoUsd = {
                'BTC':{'2019-12-23':1000, '2019-12-24':1100, '2019-12-25':1200, '2019-12-26':1300,  },
                'ETH':{'2019-12-23':100, '2019-12-24':110, '2019-12-25':120, '2019-12-26':130,  },
        }

precoDolarBrlCompra = {'2019-12-23':2.00, '2019-12-24':2.1, '2019-12-25':2.2, '2019-12-26':2.3,  }
precoDolarBrlVenda = {'2019-12-23':2.00, '2019-12-24':2.1, '2019-12-25':2.2, '2019-12-26':2.3, }


regs = [
        
    # deposita BRL
    {'origem': 'a1', 
     'idop': 1577145444.0, 
     'UTC_Time': pd.Timestamp('2019-12-23 20:57:24+0000', tz='UTC'), 
     'Operation_name': 'DEPOSIT', 
     'Remark': '', 
     'Operation_type': 'deposit', 
     'Coin': 'BRL', 'Change': 1000.0,
     
     'res_sem_cotacao': {
             'carteira': {'BRL': {'qt': 1000.0, 'totalR$': 1000.0}},
             'mesames': {'201912': {'opRS': 1000.0, 'vendaRS': 0.0, 'lucroRS': 0.0}}
             },

     'res_com_cotacao': {
             'carteira': {'BRL': {'qt': 1000.0, 'totalR$': 1000.0}},
             'mesames': {'201912': {'opRS': 1000.0, 'vendaRS': 0.0, 'lucroRS': 0.0}}
             }
     
     },

    # compra BTC
    {'origem': 'a1', 
     'idop': 1577145504.0, 
     'UTC_Time': pd.Timestamp('2019-12-23 20:58:24+0000', tz='UTC'), 
     'Operation_name': 'BUY', 
     'Remark': '', 
     'Operation_type': 'buy', 
     'Coin': 'BTC', 'Change': 0.1},
     
    {'origem': 'a1', 
     'idop': 1577145504.0, 
     'UTC_Time': pd.Timestamp('2019-12-23 20:58:24+0000', tz='UTC'), 
     'Operation_name': 'BUY', 
     'Remark': '', 
     'Operation_type': 'buy', 
     'Coin': 'BRL', 'Change': -900.0,
     
     'res_sem_cotacao': {
             'carteira': {
                     'BRL': {'qt': 100.0, 'totalR$': 100.0},
                     'BTC': {'qt': 0.1, 'totalR$': 900.0}
                     },
             'mesames': {'201912': {'opRS': 1900.0, 'vendaRS': 0.0, 'lucroRS': 0.0}}
             },

     'res_com_cotacao': {
             'carteira': {'BRL': {'qt': 100.0, 'totalR$': 100.0},
                          'BTC': {'qt': 0.1, 'totalR$': 900.0}
                          },
             'mesames': {'201912': {'opRS': 1900.0, 'vendaRS': 0.0, 'lucroRS': 0.0}}
             },
     
     },
    
     
     
    
    # troca BTC por ETH
    {'origem': 'a1', 
     'idop': 1577146173.0, 
     'UTC_Time': pd.Timestamp('2019-12-23 21:09:33+0000', tz='UTC'), 
     'Operation_name': 'BUY', 
     'Remark': '', 
     'Operation_type': 'buy', 
     'Coin': 'ETH', 'Change': 1.1},
     
    {'origem': 'a1', 
     'idop': 1577146173.0, 
     'UTC_Time': pd.Timestamp('2019-12-23 21:09:33+0000', tz='UTC'), 
     'Operation_name': 'BUY', 
     'Remark': '', 
     'Operation_type': 'buy', 
     'Coin': 'BTC', 'Change': -0.05},   
     
    {'origem': 'a1', 
     'idop': 1577146173.0, 
     'UTC_Time': pd.Timestamp('2019-12-23 21:09:33+0000', tz='UTC'), 
     'Operation_name': 'BUY', 
     'Remark': '', 
     'Operation_type': 'fee', 
     'Coin': 'ETH', 'Change': -0.1,     
    
     
     'res_sem_cotacao': {
             'carteira': {'BRL': {'qt': 100.0, 'totalR$': 100.0},
                          'BTC': {'qt': 0.05, 'totalR$': 450.0},
                          'ETH': {'qt': 1.0, 'totalR$': 450.0}
                          },
             
             'mesames': {'201912': {'opRS': 2350.0, 'vendaRS': 0.0, 'lucroRS': 0.0}}
             },

     'res_com_cotacao': {
             'carteira': {
                     'BRL': {'qt': 100.0, 'totalR$': 100.0},
                     'BTC': {'qt': 0.05, 'totalR$': 450.0},
                     'ETH': {'qt': 1.0, 'totalR$': 450.0}                     
                 },
             'mesames': {'201912': {'opRS': 2350.0, 'vendaRS': 0.0, 'lucroRS': 0.0}}
             },     
    },
    
    # vende ETH com lucro
    {'origem': 'a1', 
     'idop': 1577195504.0, 
     'UTC_Time': pd.Timestamp('2019-12-24 20:58:24+0000', tz='UTC'), 
     'Operation_name': 'BUY', 
     'Remark': '', 
     'Operation_type': 'buy', 
     'Coin': 'BRL', 'Change': 1000.0},
     
    {'origem': 'a1', 
     'idop': 1577195504.0, 
     'UTC_Time': pd.Timestamp('2019-12-24 20:58:24+0000', tz='UTC'), 
     'Operation_name': 'BUY', 
     'Remark': '', 
     'Operation_type': 'buy', 
     'Coin': 'ETH', 'Change': -0.5,     
    
     
     'res_sem_cotacao': {
             'carteira': {'BRL': {'qt': 1100.0, 'totalR$': 1100.0},
                          'BTC': {'qt': 0.05, 'totalR$': 450.0},
                          'ETH': {'qt': 0.5, 'totalR$': 225.0}
                          },
             
             'mesames': {'201912': {'opRS': 3350.0, 'vendaRS': 1000.0, 'lucroRS': 775.0}}
             },

     'res_com_cotacao': {
             'carteira': {
                     'BRL': {'qt': 1100.0, 'totalR$': 1100.0},
                     'BTC': {'qt': 0.05, 'totalR$': 450.0},
                     'ETH': {'qt': 0.5, 'totalR$': 225.0}                     
                 },
             'mesames': {'201912': {'opRS': 3350.0, 'vendaRS': 1000.0, 'lucroRS': 775.0}}
             },     
    },     
     
    # vende BTC com lucro
    {'origem': 'a1', 
     'idop': 1577199504.0, 
     'UTC_Time': pd.Timestamp('2019-12-25 20:58:24+0000', tz='UTC'), 
     'Operation_name': 'SELL', 
     'Remark': '', 
     'Operation_type': 'sell', 
     'Coin': 'BRL', 'Change': 400.0},
     
    {'origem': 'a1', 
     'idop': 1577199504.0, 
     'UTC_Time': pd.Timestamp('2019-12-25 20:58:24+0000', tz='UTC'), 
     'Operation_name': 'SELL', 
     'Remark': '', 
     'Operation_type': 'sell', 
     'Coin': 'BTC', 'Change': -0.0099},         

    {'origem': 'a1', 
     'idop': 1577199504.0, 
     'UTC_Time': pd.Timestamp('2019-12-25 20:58:24+0000', tz='UTC'), 
     'Operation_name': 'SELL', 
     'Remark': '', 
     'Operation_type': 'fee', 
     'Coin': 'BTC', 'Change': -0.0001},         

    # retira BRL     
    {'origem': 'a1', 
     'idop': 1577200000.0, 
     'UTC_Time': pd.Timestamp('2019-12-25 21:58:24+0000', tz='UTC'), 
     'Operation_name': 'WITHDRAW', 
     'Remark': '', 
     'Operation_type': 'withdraw', 
     'Coin': 'BRL', 'Change': -900.0},        

    # retira BTC
    {'origem': 'a1', 
     'idop': 1577203000.0, 
     'UTC_Time': pd.Timestamp('2019-12-25 22:58:24+0000', tz='UTC'), 
     'Operation_name': 'WITHDRAW', 
     'Remark': '', 
     'Operation_type': 'withdraw', 
     'Coin': 'BTC', 'Change': -0.015},        

     
    # deposita ETH
    {'origem': 'a1', 
     'idop': 1577206000.0, 
     'UTC_Time': pd.Timestamp('2019-12-25 23:58:24+0000', tz='UTC'), 
     'Operation_name': 'DEPOSIT', 
     'Remark': 'ValRS=20.0', 
     'Operation_type': 'deposit', 
     'Coin': 'ETH', 'Change': 0.01},      
     
     
    # recebe staking ETH
    {'origem': 'a1', 
     'idop': 1577208000.0, 
     'UTC_Time': pd.Timestamp('2019-12-26 01:58:24+0000', tz='UTC'), 
     'Operation_name': 'Staking Rewards', 
     'Remark': '', 
     'Operation_type': 'deposit', 
     'Coin': 'ETH', 'Change': 0.0001},      
     
     
    # vende ETH com prejuizo
    {'origem': 'a1', 
     'idop': 1577211000.0, 
     'UTC_Time': pd.Timestamp('2019-12-26 02:58:24+0000', tz='UTC'), 
     'Operation_name': 'SELL', 
     'Remark': '', 
     'Operation_type': 'sell', 
     'Coin': 'BRL', 'Change': 100.0},
     
    {'origem': 'a1', 
     'idop': 1577211000.0, 
     'UTC_Time': pd.Timestamp('2019-12-26 02:58:24+0000', tz='UTC'), 
     'Operation_name': 'SELL', 
     'Remark': '', 
     'Operation_type': 'sell', 
     'Coin': 'ETH', 'Change': -0.3},      
     
    ]




def teste_sem_cotacao(n, regs):
    
    ok = True
    
    cctpat = CarregaTransacoes_PAT.CarregaTransacoes_PAT('Teste')
    cctpat.hc =  None
    
    cartf = regs[-1]['res_sem_cotacao']['carteira']
    mmf   = regs[-1]['res_sem_cotacao']['mesames']
           
    rett, mesames = cctpat.carregaTransacoes(regs)
    if  cctpat.carteira.moedas != cartf:
        ok = False
        print("  ERRO %d.0"%n)
        print("esperado", cartf)
        print("obtido  ", cartTeste.moedas)
        
    if cctpat.mesames != mmf:
        ok = False
        print("  ERRO %d.1"%n)
        print("esperado", mmf)
        print("obtido  ", mesames)
        
        
    print("teste", n, "OK" if ok else "NOK")
        
    return ok




# -------------------------------------
if __name__ == "__main__":
    ok = True
    
    for i in range(len(regs)):
        if 'res_sem_cotacao' in regs[i]:
            ok = ok and teste_sem_cotacao(i, regs[:i+1])
            
    
    
    print("Final:", "OK" if ok else "NOK")
        
        
        