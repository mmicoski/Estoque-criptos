# Estoque-criptos
Computa o saldo de criptos a partir dos relatórios de operações nas corretoras.


## Carteira.py
Define a classe **Carteira**, que mantém a quantidade de cada cripto e o valor de compra, em R$.
<br><br>

## CarregaTransacoes.py
Lê transações no formato padrão e atualiza uma Carteira.<br>

Trabalha com o conceito de "permuta", isto é, só considera venda, com lucro passível de imposto, quando uma cripto é trocada por BRL.

Acumula o total de operações, o total de vendas e o lucro para cada mês.<br>
Gera relatório informando a necessidade de declarar as operações (no caso de exchange estrangeira) e de pagar imposto.
<br><br>


## Testa_CarregaTransacoes.py
Casos de teste para CarregaTransacoes.py
<br><br>

## AcumulaOperacoesBinance.py
A classe **LeOperacoesBinance** lê os formatos da Binance, como Depositos, Trades e Transacoes. <br>

Aviso: o relatório mais completo da Binance é o Transactions. Como esse relatório foi adicionado recentemente, uso outros relatórios para dados mais antigos. Por isso ainda é necessário trabalhar na detecção de registros duplicados e completar a função LeOperacoesBinance::leArquivoTransactions().

O main traz um exemplo de uso, usando a classe **LeOperacoesBinance** e salvando os registros em um arquivo com formato padrão similar ao do relatório de transações.

Na sequencia, lê os registros do formato padrão usando o mõdulo **CarregaTransacoes.py**  e acumula os valores na carteira usando **Carteira.py**
<br><br>

## AcumulaOperacoesBitcoinTrade.py
A classe **LeOperacoesBitcointrade** lê o extrato da Bitcointrade. <br>

O main traz um exemplo de uso, usando a classe **LeOperacoesBitcointrade** e salvando os registros em um arquivo com formato padrão.

Na sequencia, lê os registros do formato padrão usando o mõdulo **CarregaTransacoes.py**  e acumula os valores na carteira usando **Carteira.py**
