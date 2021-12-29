# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 12:08:49 2021

@author: mmico
"""

# testes
import Carteira
import CarregaTransacoes
import pandas as pd 


cartTeste = None

regs = [
        
    # deposita BRL
    {'origem': 'a1', 
     'idop': 1577145444.0, 
     'UTC_Time': pd.Timestamp('2019-12-23 20:57:24+0000', tz='UTC'), 
     'Operation_name': 'DEPOSIT', 
     'Remark': '', 
     'Operation_type': 'deposit', 
     'Coin': 'BRL', 'Change': 1000.0},

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
     'Coin': 'BRL', 'Change': -900.0},
    
    
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
     'Coin': 'ETH', 'Change': -0.1},     
    
    
    # vende ETH
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
     'Coin': 'ETH', 'Change': -0.5},     
     
    # vende BTC
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
     
    ]


testes = [
        # teste 0
        [0,1,
         {'BRL': {'qt': 1000.0, 'totalR$': 1000.0}},
         {'201912': {'opRS': 1000.0, 'vendaRS': 0.0, 'lucroRS': 0.0}}
         ],
        
        
        # teste 1
        [0,3,
         {'BRL': {'qt': 100.0, 'totalR$': 100.0},
             'BTC': {'qt': 0.1, 'totalR$': 900.0}
             },
         {'201912': {'opRS': 1900.0, 'vendaRS': 0.0, 'lucroRS': 0.0}}
         ],
        
        # teste 2
        [0,6,
         {'BRL': {'qt': 100.0, 'totalR$': 100.0},
             'BTC': {'qt': 0.05, 'totalR$': 450.0},
             'ETH': {'qt': 1.0, 'totalR$': 450.0}
             },
         {'201912': {'opRS': 2350.0, 'vendaRS': 0.0, 'lucroRS': 0.0}}
         ],        
        
        # teste 3
        [0,8,
         {'BRL': {'qt': 1100.0, 'totalR$': 1100.0},
             'BTC': {'qt': 0.05, 'totalR$': 450.0},
             'ETH': {'qt': 0.5, 'totalR$': 225.0}
             },
         {'201912': {'opRS': 2575.0, 'vendaRS': 1000.0, 'lucroRS': 775.0}}
         ],   


        # teste 4
         [0,11,
         {'BRL': {'qt': 1500.0, 'totalR$': 1500.0},
             'BTC': {'qt': 0.04, 'totalR$': 360.0},
             'ETH': {'qt': 0.5, 'totalR$': 225.0}
             },
         {'201912': {'opRS': 2665.0, 'vendaRS': 1400.0, 'lucroRS': 1085.0}}
         ],  


        # teste 5
         [0,12,
         {'BRL': {'qt': 600.0, 'totalR$': 600.0},
             'BTC': {'qt': 0.04, 'totalR$': 360.0},
             'ETH': {'qt': 0.5, 'totalR$': 225.0}
             },
         {'201912': {'opRS': 3565.0, 'vendaRS': 1400.0, 'lucroRS': 1085.0}}
         ],  
        
        # teste 6
         [0,13,
         {'BRL': {'qt': 600.0, 'totalR$': 600.0},
             'BTC': {'qt': 0.025, 'totalR$': 225.0},
             'ETH': {'qt': 0.5, 'totalR$': 225.0}
             },
         {'201912': {'opRS': 3700.0, 'vendaRS': 1400.0, 'lucroRS': 1085.0}}
         ],  
         
        # teste 7
         [0,14,
         {'BRL': {'qt': 600.0, 'totalR$': 600.0},
             'BTC': {'qt': 0.025, 'totalR$': 225.0},
             'ETH': {'qt': 0.51, 'totalR$': 245.0}
             },
         {'201912': {'opRS': 3720.0, 'vendaRS': 1400.0, 'lucroRS': 1085.0}}
         ],  

        # teste 8
         [0,15,
         {'BRL': {'qt': 600.0, 'totalR$': 600.0},
             'BTC': {'qt': 0.025, 'totalR$': 225.0},
             'ETH': {'qt': 0.5101, 'totalR$': 245.0}
             },
         {'201912': {'opRS': 3720.0, 'vendaRS': 1400.0, 'lucroRS': 1085.0}}
         ],  



        ]

def teste(n, regs, cartf, mmf):
    global cartTeste
    
    ok = True
    
    cartTeste = Carteira.Carteira('TesteRS',{})
    CarregaTransacoes.mesames = {} 
           
    rett, mesames = CarregaTransacoes.carregaTransacoes(cartTeste, regs)
    if  cartTeste.moedas != cartf:
        ok = False
        print("  ERRO %d.0"%n)
        print("esperado", cartf)
        print("obtido  ", cartTeste.moedas)
        
    if CarregaTransacoes.mesames != mmf:
        ok = False
        print("  ERRO %d.1"%n)
        print("esperado", mmf)
        print("obtido  ", mesames)
        
        
    print("teste", n, "OK" if ok else "NOK")
        
    return ok




# -------------------------------------
if __name__ == "__main__":
    ok = True
    
    for i,t in enumerate(testes):
        ok = ok and teste(i, regs[t[0]:t[1]], t[2], t[3])
    
    
    print("Final:", "OK" if ok else "NOK")
        
        
        