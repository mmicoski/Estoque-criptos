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
        
    # 0 deposita BRL
    {'origem': 'a1', 
     'idop': 1577145444.0, 
     'UTC_Time': pd.Timestamp('2019-12-23 20:57:24+0000', tz='UTC'), 
     'Operation_name': 'DEPOSIT', 
     'Remark': '', 
     'Operation_type': 'deposit', 
     'Coin': 'BRL', 'Change': 1000.0,
     
     
      'carteira':   {'BRL': {'qt': 1000.0, 'totalR$': 1000.0}},
      'mesames':   {'201912': {'opRS': 1000.0, 'vendaRS': 0.0, 'lucroRS': 0.0}}
     
     },

    # 1 compra BTC
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
    
      'carteira':   {'BRL': {'qt': 100.0, 'totalR$': 100.0},
                     'BTC': {'qt':   0.1, 'totalR$': 900.0},
                     },
      'mesames':   {'201912': {'opRS': 1900.0, 'vendaRS': 0.0, 'lucroRS': 0.0}}
      },
    
    # 3 troca BTC por ETH
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
    
      'carteira':   {'BRL': {'qt': 100.00, 'totalR$': 100.0},
                     'BTC': {'qt':   0.05, 'totalR$': 450.0},
                     'ETH': {'qt':   1.00, 'totalR$': 450.0},
                     },
      'mesames':   {'201912': {'opRS': 2350.0, 'vendaRS': 0.0, 'lucroRS': 0.0}}
      },
    
    # 6 vende ETH com lucro
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
     
     
      'carteira':   {'BRL': {'qt': 1100.00, 'totalR$': 1100.0},
                     'BTC': {'qt':    0.05, 'totalR$': 450.0},
                     'ETH': {'qt':    0.50, 'totalR$': 225.0},
                     },
      'mesames':   {'201912': {'opRS': 3350.0, 'vendaRS': 1000.0, 'lucroRS': 775.0}}     
     },     
     
    # 8 vende BTC com lucro
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
     'Coin': 'BTC', 'Change': -0.0001,
     
     
      'carteira':   {'BRL': {'qt': 1500.00, 'totalR$': 1500.0},
                     'BTC': {'qt':    0.04, 'totalR$': 360.0},
                     'ETH': {'qt':    0.50, 'totalR$': 225.0},
                     },
      'mesames':   {'201912': {'opRS': 3750.0, 'vendaRS': 1400.0, 'lucroRS': 1085.0}}       
     
     },         

    # 11 retira BRL     
    {'origem': 'a1', 
     'idop': 1577200000.0, 
     'UTC_Time': pd.Timestamp('2019-12-25 21:58:24+0000', tz='UTC'), 
     'Operation_name': 'WITHDRAW', 
     'Remark': '', 
     'Operation_type': 'withdraw', 
     'Coin': 'BRL', 'Change': -900.0,
     
     
      'carteira':   {'BRL': {'qt':  600.00, 'totalR$': 600.0},
                     'BTC': {'qt':    0.04, 'totalR$': 360.0},
                     'ETH': {'qt':    0.50, 'totalR$': 225.0},
                     },
      'mesames':   {'201912': {'opRS': 4650.0, 'vendaRS': 1400.0, 'lucroRS': 1085.0}}       
          
     },        

    # 12 retira BTC
    {'origem': 'a1', 
     'idop': 1577203000.0, 
     'UTC_Time': pd.Timestamp('2019-12-25 22:58:24+0000', tz='UTC'), 
     'Operation_name': 'WITHDRAW', 
     'Remark': '', 
     'Operation_type': 'withdraw', 
     'Coin': 'BTC', 'Change': -0.015,
     
     'carteira':   {'BRL': {'qt':  600.00, 'totalR$': 600.0},
                     'BTC': {'qt':    0.025, 'totalR$': 225.0},
                     'ETH': {'qt':    0.50, 'totalR$': 225.0},
                     },
      'mesames':   {'201912': {'opRS': 4785.0, 'vendaRS': 1400.0, 'lucroRS': 1085.0}}       
     },        

     
    # 13 deposita ETH
    {'origem': 'a1', 
     'idop': 1577206000.0, 
     'UTC_Time': pd.Timestamp('2019-12-25 23:58:24+0000', tz='UTC'), 
     'Operation_name': 'DEPOSIT', 
     'Remark': 'ValRS=20.0', 
     'Operation_type': 'deposit', 
     'Coin': 'ETH', 'Change': 0.01,
     
     'carteira':   {'BRL': {'qt':  600.00, 'totalR$': 600.0},
                     'BTC': {'qt':    0.025, 'totalR$': 225.0},
                     'ETH': {'qt':    0.51, 'totalR$': 245.0},
                     },
      'mesames':   {'201912': {'opRS': 4805.0, 'vendaRS': 1400.0, 'lucroRS': 1085.0}}       
     },      
     
     
    # 14 recebe staking ETH
    {'origem': 'a1', 
     'idop': 1577208000.0, 
     'UTC_Time': pd.Timestamp('2019-12-26 01:58:24+0000', tz='UTC'), 
     'Operation_name': 'Staking Rewards', 
     'Remark': '', 
     'Operation_type': 'deposit', 
     'Coin': 'ETH', 'Change': 0.0001,
     
     'carteira':   {'BRL': {'qt':  600.00, 'totalR$': 600.0},
                     'BTC': {'qt':    0.025, 'totalR$': 225.0},
                     'ETH': {'qt':    0.5101, 'totalR$': 245.0},
                     },
      'mesames':   {'201912': {'opRS': 4805.0, 'vendaRS': 1400.0, 'lucroRS': 1085.0}}       
     
     },      
     
     
    # 15 vende ETH com prejuizo
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
     'Coin': 'ETH', 'Change': -0.3,
     
     'carteira':   {'BRL': {'qt':  700.00, 'totalR$': 700.0},
                     'BTC': {'qt':    0.025, 'totalR$': 225.0},
                     'ETH': {'qt':    0.2101, 'totalR$': 100.91060576357},
                     },
      'mesames':   {'201912': {'opRS': 4905.0, 'vendaRS': 1500.0, 'lucroRS': 1085.0}}       
     
     },      
     
    ]

log = False
# ----------------------------------------------
def mesmodic(dic1, dic2):
    if dic1.keys() != dic2.keys():
        if log: print(dic1.keys(), dic2.keys())
        return False
    
    for k in dic1.keys():
        if round(dic1[k],10) != round(dic2[k],10):
            if log: print(k,round(dic1[k],10), round(dic2[k],10))
            return False
        
    return True

# ----------------------------------------------
def mesmodicdic(dic1, dic2):
    if dic1.keys() != dic2.keys():
        if log: print(dic1.keys(), dic2.keys())
        return False
    
    for k in dic1.keys():
        if not mesmodic(dic1[k], dic2[k]):
            return False
        
    return True

# ----------------------------------------------
def teste(n, regs):
    global cartTeste
    
    cartf = regs[-1]['carteira']
    mmf = regs[-1]['mesames']
    
    ok = True
    
    cartTeste = Carteira.Carteira('TesteRS',{})
    CarregaTransacoes.mesames = {} 
           
    rett, mesames = CarregaTransacoes.carregaTransacoes(cartTeste, regs)
    if  not mesmodicdic(cartTeste.moedas, cartf):
        ok = False
        print("  ERRO %d.0"%n)
        print("esperado", cartf)
        print("obtido  ", cartTeste.moedas)
        
    if not mesmodicdic(CarregaTransacoes.mesames, mmf):
        ok = False
        print("  ERRO %d.1"%n)
        print("esperado", mmf)
        print("obtido  ", mesames)
        
        
    print("teste", n, "OK" if ok else "NOK")
        
    return ok




# -------------------------------------
if __name__ == "__main__":
    ok = True
    
    for i,r in enumerate(regs):
        if 'carteira' in r:
            ok = ok and teste(i, regs[:i+1])
    
    
    print("Final:", "OK" if ok else "NOK")
        
        
        