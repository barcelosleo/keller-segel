# Modelo de Keller-Segel para simulação da interação entre População e Atividade Econômica

Proposto por Evelyn Fox Keller, física norte-americana, e Lee Aaron Segel, matemático também norte-americano, o modelo de Keller-Segel foi historicamente utilizado para descrever o movimento de bactérias. Introduzido primeiramente em 1970 para descrever a agregação de uma espécie de bolor limoso (ou slime mold) ameboide, Dictyostelium discoideum, o modelo se tornou um dos mais usados nos estudos biológicos-matemáticos. As células deste slime mold se comportam como amoebas individuais, e se alimentam de bactérias, mas quando a quantidade de comida fica pequena, elas se difundem pelo espaço e então se agregam em formato mais alongado, como o formato das lesmas, para uma migração de longa distância. Keller e Segel desenvolveram um modelo matemático para o processo de agregação, em que a chemotaxis tem papel crítico na auto-ormanização das células.

Baseados no que já era conhecido sobre esses organismos, Keller e Segel utilizaram as seguintes premissas:
* As células estão inicialmente distribuídas sobre o espaço de maneira mais ou menos homogênea, com algumas flutuações aleatótias;
* As células apresentam chemotaxis em direção ao sinal químico denominado cAMP (cyclic adenosine monophosphate);
* As células produzem moléculas cAMP;
* As células e as moléculas cAMP difundem pelo espaço;
* As células não morrem e não se dividem.

## Aplicação para dinâmica população-economia
De forma parecida com as premissas de Keller e Segel, os seguintes pontos são assumidos para modelar a relação entre a população e a atividade econômica:
* A população não cresce e não decresce ao longo do tempo;
* A economia é ativada por existir mais pessoas em uma região;
* Sem pessoas a atividade econômica diminui;
* População e atividade econômica difundem gradualmente;
* As pessoas são atraídas por regiões com maior atividade econômica.

# Simulação
O método numérico utilizado, foi o **FTCS** (*Forward Time Centered Space*, em tradução livre significa "avançado no tempo, centrado no espaço), que é utilizado para a discretização de Equações Diferenciais Parciais(EDP). Além disso, foi utilizado **PBC** (*Periodic Boundary Conditions*)

## Resultados 1D

### Distribuição 1
![Evolução para determinada distribuição monetária][dist1-1d]

[dist1-1d]:https://github.com/leonardob17/keller-segel/blob/main/imagens/1D-1.jpeg

### Distribuição 2
![Evolução para determinada distribuição monetária][dist2-1d]

[dist2-1d]:https://github.com/leonardob17/keller-segel/blob/main/imagens/1D-2.jpeg

### Distribuição 3
![Evolução para determinada distribuição monetária][dist3-1d]

[dist3-1d]:https://github.com/leonardob17/keller-segel/blob/main/imagens/1D-3.jpeg

## Resultados 2D
Para todos os exemplos a seguir, foram utilizadas distribuições populacionais homogêneas no espaço.

### Distribuição 1
![Evolução para determinada distribuição monetária][dist1-2d]

[dist1-2d]:https://github.com/leonardob17/keller-segel/blob/main/imagens/comparacao_tempos.png

![Animação][dist1-2d-gif]

[dist1-2d-gif]:https://github.com/leonardob17/keller-segel/blob/main/imagens/dinamica_pop_eco_2d.gif

### Distribuição 2
![Evolução para determinada distribuição monetária][dist2-2d]

[dist2-2d]:https://github.com/leonardob17/keller-segel/blob/main/imagens/comparacao_tempos_dinheiro_desuniforme.png

![Animação][dist2-2d-gif]

[dist2-2d-gif]:https://github.com/leonardob17/keller-segel/blob/main/imagens/dinamica_pop_eco_2d_dinheiro_desuniform.gif

### Distribuição 3
![Evolução para determinada distribuição monetária][dist3-2d]

[dist3-2d]:https://github.com/leonardob17/keller-segel/blob/main/imagens/comparacao_tempos_pop_uniforme_sem_dinheiro.png

![Animação][dist3-2d-gif]

[dist3-2d-gif]:https://github.com/leonardob17/keller-segel/blob/main/imagens/dinamica_pop_eco_2d_pop_uniforme_sem_dinheiro.gif

# Wiki
Versão completa das discretizações na [Wiki do Instituto de Física da UFRGS](https://fiscomp.if.ufrgs.br/index.php/Modelo_de_Keller-Segel_para_rela%C3%A7%C3%A3o_popula%C3%A7%C3%A3o-economia)
