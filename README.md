# Sistema de Pedidos e Faturamento — UNIARP (2026)

Este sistema foi desenvolvido como atividade prática para a disciplina de **Estrutura de Dados** (3ª Fase / 2026) da **UNIARP**, sob a orientação do Prof. Emanuel Tonis Florz.

O objetivo do projeto é gerir produtos, pedidos e o faturamento de um estabelecimento utilizando **Python 3** com interface gráfica em **Tkinter** e armazenamento local persistente em arquivos **CSV**.

## 🚀 Funcionalidades Principais

1. **Gestão de Produtos:** Cadastro e listagem de itens (Bebidas ou Lanches) com validação de ID, descrição e preço.
2. **Gestão de Pedidos:** Lançamento de novos consumos associados a mesas específicas com incremento automático de IDs.
3. **Fechamento de Mesa:** Consulta de todos os pedidos ativos de uma mesa, cálculo automático do total consumido e encerramento da conta.
4. **Relatórios:** Filtro de faturamento geral por período (datas) e segmentação de lucros por tipo de produto.

---

## 📂 Estrutura de Arquivos

```text
sistema/
├── dados/                       # Pasta criada automaticamente com os arquivos .csv
├── lib/                         # Pacote com os submódulos do sistema
│   ├── __init__.py              # Inicializador do pacote
│   ├── arquivos.py              # Leitura, gravação e persistência de dados (CSV)
│   ├── fechamento.py            # Lógica e interface de encerramento de mesas
│   ├── interface.py             # Configurações visuais, paleta de cores e estilos
│   ├── pedidos.py               # Lógica e interface para lançar novos pedidos
│   ├── produtos.py              # Cadastro e exibição em tabela dos produtos
│   ├── relatorios.py            # Filtros de faturamento e exibição de relatórios
│   └── validacoes.py            # Regras de negócio (datas, valores e tipos válidos)
└── sistema.py                   # Ponto de entrada do programa (Menu Principal)
```

## Para instalação do .exe / .elf:
```
pyinstaller --noconfirm --onefile --windowed \
--collect-all="matplotlib" \
--collect-all="pandas" \
--hidden-import="mplcursors" \
--add-data="dados:dados" \
--add-data="lib:lib" \
sistema.py
```