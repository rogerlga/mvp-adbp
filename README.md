# MVP Análise de Dados e Boas Práticas

Este projeto aplica técnicas de **análise exploratória** e de **pré-processamento** nos dados operacionais de um turbogerador a gás, de forma a preparar o dataset para o treinamento de futuros modelos. O notebook resultado desse trabalho é a entrega do MVP do curso de pós-graduação em *Ciência de Dados & Analytics* da PUC-Rio (2025).

O notebook pode ser encontrado em:
- Neste repositório do GitHub: [mvp_adbp.ipynb (GitHub)](mvp_adbp.ipynb)
- Link para abertura no Google Colab: [mvp_adbp.ipynb (Colab)](https://colab.research.google.com/github/rogerlga/mvp-adbp/blob/main/mvp_adbp.ipynb)

## Descrição

Os dados contém medições de sensores de um trem de geração elétrica, formado por Turbina a Gás (Gas Generator/GG + Power Turbine/PT), Caixa de Engrenagem (Gearbox) e Gerador Elétrico (Generator), representado na ilustração abaixo:

<img src="https://raw.githubusercontent.com/rogerlga/mvp-adbp/refs/heads/main/assets/two_shaft_turbogenerator.jpg" width="600">

*Trem de equipamentos (fonte imagem: [site](http://emadrlc.blogspot.com/2013/01/chapter-1-introduction-to-gas-turbines.html))*

Uma análise geral é feita no conjunto completo e posteriormente o foco da análise vai para a Turbina a Gás:

<img src="https://raw.githubusercontent.com/rogerlga/mvp-adbp/refs/heads/main/assets/TG_tags.png" width="700">

*Representação de uma Turbina a Gás com os atributos do dataset (fonte imagem: adaptado do [site](https://www.researchgate.net/figure/Schematic-of-LM2500-marine-gas-turbine_fig1_349497740) pelo autor)*

Os resultados são bastante satisfatórios, gerando ao final um dataset preparado para uso no treinamento de modelos, que será tema de trabalhos futuros.

## Hipóteses

As hipóteses levantadas para o problema são:

- Existe correlação entre as variáveis, de forma que futuramente poderemos predizer um atributo target a partir dos demais;
- Não há dados anômalos suficientes na indústria, o que dificulta treinos supervisionados para detecção de anomalias;
- É possível distinguir diferentes perfis operacionais através dos dados, visando futuramente treinar um modelo que faça a classificação automática desses perfis.

## Objetivos

Os objetivos desse estudo vão permear em torno de **preparar o dataset para**:

- Treinar um modelo **supervisionado** que preveja os valores de temperatura de exaustão da turbina a partir das demais tags (em condição normal), visando comparar valores reais com as predições, o que dará um indicativo da eficiência do equipamento;
- Treinar um modelo **não supervisionado** que detecte os períodos em que o equipamento está apresentando comportamento anômalo (pré-falha). A base de dados será o período sabido como "normal", não havendo rótulos de anomalias. Serão considerados anômalos os comportamentos diferentes daqueles aprendidos como "normais";
- Treinar um modelo **nâo supervisionado** para classificação automática dos distintos perfis operacionais, como operação com gás, operação com diesel, turbina em carga base, em carga parcial, partida, parada, etc.
