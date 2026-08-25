# EcoCharge Smart Grid

O **EcoCharge Smart Grid** é um protótipo acadêmico desenvolvido para o **Challenge GoodWe 2026**, com foco no gerenciamento inteligente da recarga de veículos elétricos.

O sistema busca reduzir problemas relacionados à alta demanda de energia em estações de recarga, utilizando distribuição inteligente de potência, priorização de veículos e monitoramento do consumo.

## Funcionalidades

- Gerenciamento inteligente da potência disponível
- Priorização de veículos com baixa bateria e necessidade urgente
- Redistribuição automática da energia
- Simulação de geração de energia solar
- Monitoramento do nível de bateria
- Monitoramento da potência destinada a cada veículo
- Cálculo do consumo energético em kWh
- Cálculo automático do custo da recarga
- Finalização da sessão de recarga
- Simulação de pagamento
- Conexão de novos veículos
- Painel de telemetria da rede

## Como funciona

O EcoCharge considera a capacidade disponível da rede elétrica e a geração de energia solar.

Quando vários veículos estão conectados simultaneamente, o sistema analisa fatores como nível de bateria e prioridade da recarga para distribuir a potência disponível.

Veículos classificados como urgentes recebem prioridade, enquanto o sistema procura manter a demanda dentro dos limites disponíveis.

## Tecnologias utilizadas

- Python
- Streamlit
- Pandas
- HTML/CSS integrado ao Streamlit

## Como executar

Primeiro, instale as dependências:

```bash
pip install -r requirements.txt
```

Depois execute:

```bash
python -m streamlit run app.py
```

O sistema será aberto automaticamente no navegador.

## Observação

Este projeto é um **protótipo acadêmico**. Os veículos, valores de potência, geração solar, consumo energético e pagamentos apresentados na aplicação são simulados para fins de demonstração.

## Equipe

- Lucca Bertolini - RM: 569552
- Diego de Oliveira Brandão - RM: 569773
- Raphaello Caffettani - RM: 572334
- Cristhian Henrique Clementino - RM: 574117
- Fabio Pena Vieira - RM: 570441

**Challenge GoodWe 2026**  
Ciência da Computação — FIAP
