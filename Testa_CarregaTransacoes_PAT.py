# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 12:08:49 2021

@author: mmico
"""

# testes

import CarregaTransacoes_PAT
import pandas as pd 


precoCriptoUsd = {
                'BTC':{'2019-12-23':10000, '2019-12-24':11000, '2019-12-25':12000, '2019-12-26':13000,  },
                'ETH':{'2019-12-23':100, '2019-12-24':200, '2019-12-25':300, '2019-12-26':60,  },
        }

precoDolarBrlCompra = {'2019-12-23':2.00, '2019-12-24':2.1, '2019-12-25':2.2, '2019-12-26':2.3,  }
precoDolarBrlVenda = {'2019-12-23':2.00, '2019-12-24':2.1, '2019-12-25':2.2, '2019-12-26':2.3, }


regs = [
        
    # 0 deposita BRL
    {'origem': 'a1', 
     'idop': 1577145444.0, 
     'UTC_Time': pd.Timestamp('2019-12-23 20:57:24+0000', tz='UTC'), 
     'Operation_name': 'DEPOSIT', 
     'Remark': '', 
     'Operation_type': 'deposit', 
     'Coin': 'BRL', 'Change': 1000.0,
     
     # -------------------
     'res_sem_cotacao': {
             'carteira': {'BRL': {'qt': 1000.0, 'totalR$': 1000.0}},
             'mesames': {'201912': {'opRS': 1000.0, 'vendaRS': 0.0, 'lucroRS': 0.0}}
             },

     # ============== 
     'res_com_cotacao': {
             'carteira': {'BRL': {'qt': 1000.0, 'totalR$': 1000.0}},
             'mesames': {'201912': {'opRS': 1000.0, 'vendaRS': 0.0, 'lucroRS': 0.0}}
             }
     
     },

    # 1 compra BTC
    {'origem': 'a1', 
     'idop': 1577145504.0, 
     'UTC_Time': pd.Timestamp('2019-12-23 20:58:24+0000', tz='UTC'), 
     'Operation_name': 'BUY', 
     'Remark': '', 
     'Operation_type': 'buy', 
     'Coin': 'BTC', 'Change': 0.045},
     
    {'origem': 'a1', 
     'idop': 1577145504.0, 
     'UTC_Time': pd.Timestamp('2019-12-23 20:58:24+0000', tz='UTC'), 
     'Operation_name': 'BUY', 
     'Remark': '', 
     'Operation_type': 'buy', 
     'Coin': 'BRL', 'Change': -900.0,
     
     # -------------------
     'res_sem_cotacao': {
             'carteira': {
                     'BRL': {'qt': 100.0, 'totalR$': 100.0},
                     'BTC': {'qt': 0.045, 'totalR$': 900.0}
                     },
             'mesames': {'201912': {'opRS': 1900.0, 'vendaRS': 0.0, 'lucroRS': 0.0}}
             },

     # ============== 
     'res_com_cotacao': {
             'carteira': {'BRL': {'qt': 100.0, 'totalR$': 100.0},
                          'BTC': {'qt': 0.045, 'totalR$': 900.0}
                          },
             'mesames': {'201912': {'opRS': 1900.0, 'vendaRS': 0.0, 'lucroRS': 0.0}}
             },
     
     },
    
     
     
    
    # 3 troca BTC por ETH
    {'origem': 'a1', 
     'idop': 1577146173.0, 
     'UTC_Time': pd.Timestamp('2019-12-24 19:09:33+0000', tz='UTC'), 
     'Operation_name': 'BUY', 
     'Remark': '', 
     'Operation_type': 'buy', 
     'Coin': 'ETH', 'Change': 1.2},
     
    {'origem': 'a1', 
     'idop': 1577146173.0, 
     'UTC_Time': pd.Timestamp('2019-12-24 19:09:33+0000', tz='UTC'), 
     'Operation_name': 'BUY', 
     'Remark': '', 
     'Operation_type': 'buy', 
     'Coin': 'BTC', 'Change': -0.02},   
     
    {'origem': 'a1', 
     'idop': 1577146173.0, 
     'UTC_Time': pd.Timestamp('2019-12-24 19:09:33+0000', tz='UTC'), 
     'Operation_name': 'BUY', 
     'Remark': '', 
     'Operation_type': 'fee', 
     'Coin': 'ETH', 'Change': -0.1,     
    
     # -------------------
     'res_sem_cotacao': {
             'carteira': {'BRL': {'qt': 100.0, 'totalR$': 100.0},
                          'BTC': {'qt': 0.025, 'totalR$': 500.0},
                          'ETH': {'qt': 1.1, 'totalR$': 400.0}
                          },
             
             'mesames': {'201912': {'opRS': 2300.0, 'vendaRS': 0.0, 'lucroRS': 0.0}}
             },

     # ============== 
     'res_com_cotacao': {
             'carteira': {
                         'BRL': {'qt': 100.0, 'totalR$': 100.0},
                         'BTC': {'qt': 0.025, 'totalR$': 500.0},
                         'ETH': {'qt': 1.1, 'totalR$': 462.0}                    
                 },
             'mesames': {'201912': {'opRS': 2362.0, 'vendaRS': 462.0, 'lucroRS': 62.0}}
             },     
    },
    
    # 6 vende ETH com lucro
    {'origem': 'a1', 
     'idop': 1577195504.0, 
     'UTC_Time': pd.Timestamp('2019-12-24 20:58:24+0000', tz='UTC'), 
     'Operation_name': 'BUY', 
     'Remark': '', 
     'Operation_type': 'buy', 
     'Coin': 'BRL', 'Change': 210.0},
     
    {'origem': 'a1', 
     'idop': 1577195504.0, 
     'UTC_Time': pd.Timestamp('2019-12-24 20:58:24+0000', tz='UTC'), 
     'Operation_name': 'BUY', 
     'Remark': '', 
     'Operation_type': 'buy', 
     'Coin': 'ETH', 'Change': -0.5,     
    
     
     # -------------------
     'res_sem_cotacao': {
             'carteira': {'BRL': {'qt': 310.0, 'totalR$': 310.0},
                          'BTC': {'qt': 0.025, 'totalR$': 500.0},
                          'ETH': {'qt': 0.6, 'totalR$': 218.1818181818}
                          },
             
             'mesames': {'201912': {'opRS': 2510.0, 'vendaRS': 210.0, 'lucroRS': 28.1818181818}}
             },

     # ============== 
     'res_com_cotacao': {
             'carteira': {'BRL': {'qt': 310.0, 'totalR$': 310.0},
                          'BTC': {'qt': 0.025, 'totalR$': 500.0},
                          'ETH': {'qt': 0.6, 'totalR$': 252.0}
                          },
             
             'mesames': {'201912': {'opRS': 2572.0, 'vendaRS': 672.0, 'lucroRS': 62.0}}
             },     
    },     
     
    # 8 vende BTC com lucro
    {'origem': 'a1', 
     'idop': 1577199504.0, 
     'UTC_Time': pd.Timestamp('2019-12-25 20:58:24+0000', tz='UTC'), 
     'Operation_name': 'SELL', 
     'Remark': '', 
     'Operation_type': 'sell', 
     'Coin': 'BRL', 'Change': 264.0},
     
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
     
     # -------------------
     'res_sem_cotacao': {
             'carteira': {'BRL': {'qt': 574.0, 'totalR$': 574.0},
                          'BTC': {'qt': 0.015, 'totalR$': 300.0},
                          'ETH': {'qt': 0.6, 'totalR$': 218.1818181818}
                          },
             
             'mesames': {'201912': {'opRS': 2774.0, 'vendaRS': 474.0, 'lucroRS': 92.1818181818}}
             },

     # ============== 
     'res_com_cotacao': {
             'carteira': {'BRL': {'qt': 574.0, 'totalR$': 574.0},
                          'BTC': {'qt': 0.015, 'totalR$': 300.0},
                          'ETH': {'qt': 0.6, 'totalR$': 252.0}
                          },
             'mesames': {'201912': {'opRS': 2836.0, 'vendaRS': 936.0, 'lucroRS': 126.0}}
             },         
     
     },         

    # 11 retira BRL     
    {'origem': 'a1', 
     'idop': 1577200000.0, 
     'UTC_Time': pd.Timestamp('2019-12-25 21:58:24+0000', tz='UTC'), 
     'Operation_name': 'WITHDRAW', 
     'Remark': '', 
     'Operation_type': 'withdraw', 
     'Coin': 'BRL', 'Change': -200.0,

     # -------------------
     'res_sem_cotacao': {
             'carteira': {'BRL': {'qt': 374.0, 'totalR$': 374.0},
                          'BTC': {'qt': 0.015, 'totalR$': 300.0},
                          'ETH': {'qt': 0.6, 'totalR$': 218.1818181818}
                          },
             
             'mesames': {'201912': {'opRS': 2974.0, 'vendaRS': 474.0, 'lucroRS': 92.1818181818}}
             },

     # ============== 
     'res_com_cotacao': {
             'carteira': {'BRL': {'qt': 374.0, 'totalR$': 374.0},
                          'BTC': {'qt': 0.015, 'totalR$': 300.0},
                          'ETH': {'qt': 0.6, 'totalR$': 252.0}
                          },
             'mesames': {'201912': {'opRS': 3036.0, 'vendaRS': 936.0, 'lucroRS': 126.0}}
             },       
     
     },        

    # 12 retira BTC
    {'origem': 'a1', 
     'idop': 1577203000.0, 
     'UTC_Time': pd.Timestamp('2019-12-25 22:58:24+0000', tz='UTC'), 
     'Operation_name': 'WITHDRAW', 
     'Remark': '', 
     'Operation_type': 'withdraw', 
     'Coin': 'BTC', 'Change': -0.01,
     
     # -------------------
     'res_sem_cotacao': {
             'carteira': {'BRL': {'qt': 374.0, 'totalR$': 374.0},
                          'BTC': {'qt': 0.005, 'totalR$': 100.0},
                          'ETH': {'qt': 0.6, 'totalR$': 218.1818181818}
                          },
             
             'mesames': {'201912': {'opRS': 3174.0, 'vendaRS': 474.0, 'lucroRS': 92.1818181818}}
             },

     # ============== 
     'res_com_cotacao': {
             'carteira': {'BRL': {'qt': 374.0, 'totalR$': 374.0},
                          'BTC': {'qt': 0.005, 'totalR$': 100.0},
                          'ETH': {'qt': 0.6, 'totalR$': 252.0}
                          },
             'mesames': {'201912': {'opRS': 3236.0, 'vendaRS': 936.0, 'lucroRS': 126.0}}
             },   
     },        

     
    # 13 deposita ETH
    {'origem': 'a1', 
     'idop': 1577206000.0, 
     'UTC_Time': pd.Timestamp('2019-12-25 23:58:24+0000', tz='UTC'), 
     'Operation_name': 'DEPOSIT', 
     'Remark': 'ValRS=6.6', 
     'Operation_type': 'deposit', 
     'Coin': 'ETH', 'Change': 0.01,
     
     # -------------------
     'res_sem_cotacao': {
             'carteira': {'BRL': {'qt': 374.0, 'totalR$': 374.0},
                          'BTC': {'qt': 0.005, 'totalR$': 100.0},
                          'ETH': {'qt': 0.61, 'totalR$': 224.7818181818}
                          },
             
             'mesames': {'201912': {'opRS': 3180.6, 'vendaRS': 474.0, 'lucroRS': 92.1818181818}}
             },

     # ============== 
     'res_com_cotacao': {
             'carteira': {'BRL': {'qt': 374.0, 'totalR$': 374.0},
                          'BTC': {'qt': 0.005, 'totalR$': 100.0},
                          'ETH': {'qt': 0.61, 'totalR$': 258.6}
                          },
             'mesames': {'201912': {'opRS': 3242.6, 'vendaRS': 936.0, 'lucroRS': 126.0}}
             },       
     
     },      
     
     
    # 14 recebe staking ETH
    {'origem': 'a1', 
     'idop': 1577208000.0, 
     'UTC_Time': pd.Timestamp('2019-12-26 01:58:24+0000', tz='UTC'), 
     'Operation_name': 'Staking Rewards', 
     'Remark': '', 
     'Operation_type': 'deposit', 
     'Coin': 'ETH', 'Change': 0.001,
     
     # -------------------
     'res_sem_cotacao': {
             'carteira': {'BRL': {'qt': 374.0, 'totalR$': 374.0},
                          'BTC': {'qt': 0.005, 'totalR$': 100.0},
                          'ETH': {'qt': 0.611, 'totalR$': 224.7818181818}
                          },
             
             'mesames': {'201912': {'opRS': 3180.6, 'vendaRS': 474.0, 'lucroRS': 92.1818181818}}
             },

     # ============== 
     'res_com_cotacao': {
             'carteira': {'BRL': {'qt': 374.0, 'totalR$': 374.0},
                          'BTC': {'qt': 0.005, 'totalR$': 100.0},
                          'ETH': {'qt': 0.611, 'totalR$': 258.6}
                          },
             'mesames': {'201912':  {'opRS': 3242.6, 'vendaRS': 936.0, 'lucroRS': 126.0}}
             },          
     },      
     
     
    # 15 vende ETH com prejuizo
    {'origem': 'a1', 
     'idop': 1577211000.0, 
     'UTC_Time': pd.Timestamp('2019-12-26 02:58:24+0000', tz='UTC'), 
     'Operation_name': 'SELL', 
     'Remark': '', 
     'Operation_type': 'sell', 
     'Coin': 'BRL', 'Change': 20.8518},
     
    {'origem': 'a1', 
     'idop': 1577211000.0, 
     'UTC_Time': pd.Timestamp('2019-12-26 02:58:24+0000', tz='UTC'), 
     'Operation_name': 'SELL', 
     'Remark': '', 
     'Operation_type': 'sell', 
     'Coin': 'ETH', 'Change': -0.1511,
     
     # -------------------
     'res_sem_cotacao': {
             'carteira': {'BRL': {'qt': 394.8518, 'totalR$': 394.8518},
                          'BTC': {'qt': 0.005, 'totalR$': 100.0},
                          'ETH': {'qt': 0.4599, 'totalR$': 169.193384913}
                          },
             
             'mesames': {'201912': {'opRS': 3201.4518, 'vendaRS': 494.8518, 'lucroRS': 92.1818181818}}
             },

     # ============== 
     'res_com_cotacao': {
             'carteira': {'BRL': {'qt': 394.8518, 'totalR$': 394.8518},
                          'BTC': {'qt': 0.005, 'totalR$': 100.0},
                          'ETH': {'qt': 0.4599, 'totalR$': 194.648346972177}
                          },
             'mesames': {'201912':  {'opRS': 3263.4518, 'vendaRS': 956.8518, 'lucroRS': 126.0}}
             },        
     
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
def teste_sem_cotacao(n, regs):
    
    ok = True
    
    cctpat = CarregaTransacoes_PAT.CarregaTransacoes_PAT('Teste')
    cctpat.hc =  None
    
    cartf = regs[-1]['res_sem_cotacao']['carteira']
    mmf   = regs[-1]['res_sem_cotacao']['mesames']
           
    rett, mesames = cctpat.carregaTransacoes(regs)
    if  not mesmodicdic(cctpat.carteira.moedas, cartf):
        ok = False
        print("  ERRO S%d.0"%n)
        print("esperado", cartf)
        print("obtido  ", cctpat.carteira.moedas)
        
    if not mesmodicdic(cctpat.mesames, mmf):
        ok = False
        print("  ERRO S%d.1"%n)
        print("esperado", mmf)
        print("obtido  ", mesames)
        
        
    print("teste S", n, "OK" if ok else "NOK")
        
    return ok

# ----------------------------------------------
def teste_com_cotacao(n, regs):
    
    ok = True
    
    cctpat = CarregaTransacoes_PAT.CarregaTransacoes_PAT('Teste')
    cctpat.hc.precoCriptoUsd =  precoCriptoUsd
    
    cctpat.hc.precoDolarBrlCompra = precoDolarBrlCompra
    cctpat.hc.precoDolarBrlVenda  = precoDolarBrlVenda   
    
    
    cartf = regs[-1]['res_com_cotacao']['carteira']
    mmf   = regs[-1]['res_com_cotacao']['mesames']
           
    rett, mesames = cctpat.carregaTransacoes(regs)
    if  not mesmodicdic(cctpat.carteira.moedas, cartf):
        ok = False
        print("  ERRO C%d.2"%n)
        print("esperado", cartf)
        print("obtido  ", cctpat.carteira.moedas)
        
    if not mesmodicdic(cctpat.mesames, mmf):
        ok = False
        print("  ERRO C%d.3"%n)
        print("esperado", mmf)
        print("obtido  ", mesames)
        
        
    print("teste C", n, "OK" if ok else "NOK")
        
    return ok


# -------------------------------------
if __name__ == "__main__":
    ok = True
    
    for i in range(len(regs)):
        if 'res_sem_cotacao' in regs[i]:
            ok = ok and teste_sem_cotacao(i, regs[:i+1])
            
        if 'res_com_cotacao' in regs[i]:
            ok = ok and teste_com_cotacao(i, regs[:i+1])
    
    
    print("Final:", "OK" if ok else "NOK")
        
        
        