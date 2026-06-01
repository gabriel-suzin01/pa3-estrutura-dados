import tkinter as tk
from tkinter import ttk
from datetime import datetime
from lib import interface as ui
from lib import validacoes as val
from lib import arquivos as arq

def abrir_menu_relatorios(container: tk.Frame):
    """Abre o submenu de Relatórios."""
    ui.limpar_container(container)

    tk.Label(container, text="SUBMENU: RELATÓRIOS", font=ui.FONTE_TITULO, bg=ui.COR_FUNDO, fg=ui.COR_TITULO,).pack(pady=(0, 14))

    frame = ui.frame_conteudo(container)
    frame.pack_configure(anchor="center")

    from sistema import renderizar_menu_principal

    opcoes = [
        ("1 - Faturamento Geral entre Datas", lambda: _relatorio_faturamento_geral(container)),
        ("2 - Faturamento por Tipo de Produto", lambda: _relatorio_por_tipo(container)),
        ("3 - Voltar ao Menu Principal", lambda: renderizar_menu_principal(container))]
    
    for texto, cmd in opcoes:
        ui.botao_menu(frame, texto, cmd).pack(pady=5)

#  RELATÓRIO 1 — Faturamento geral entre datas

def _relatorio_faturamento_geral(container: tk.Frame):
    ui.limpar_container(container)
    ui.frame_cabecalho(container, "⬛  FATURAMENTO GERAL ENTRE DATAS")

    frame = ui.frame_conteudo(container)

    fr_datas = tk.Frame(frame, bg=ui.COR_FUNDO)
    fr_datas.pack(fill="x", pady=(0, 6))

    tk.Label(fr_datas, text="Data Inicial (DD/MM/AAAA):", font=ui.FONTE_NORMAL, bg=ui.COR_FUNDO, fg=ui.COR_TEXTO).grid(row=0, column=0, sticky="w", padx=(0, 8))
    ent_ini = ui.entrada_campo(fr_datas, 14)
    ent_ini.grid(row=0, column=1, sticky="w")

    tk.Label(fr_datas, text="Data Final (DD/MM/AAAA):", font=ui.FONTE_NORMAL, bg=ui.COR_FUNDO, fg=ui.COR_TEXTO).grid(row=0, column=2, sticky="w", padx=(16, 8))
    ent_fim = ui.entrada_campo(fr_datas, 14)
    ent_fim.grid(row=0, column=3, sticky="w")

    ui.separador(frame)

    # Tabela de resultados
    colunas = [("data", "Data", 100), ("mesa", "Mesa", 60), ("desc", "Produto", 220), ("qtd", "Qtd", 50), ("total", "V. Total", 110)]
    fr_tree = tk.Frame(frame, bg=ui.COR_FUNDO)
    fr_tree.pack(fill="both", expand=True)
    tree = ui.criar_treeview(fr_tree, colunas, altura=11)

    ui.separador(frame)

    lbl_fat = tk.Label(frame, text="", font=("Courier New", 12, "bold"), bg=ui.COR_FUNDO, fg=ui.COR_AVISO)
    lbl_fat.pack(anchor="e", padx=10)

    def gerar():
        for item in tree.get_children():
            tree.delete(item)
        lbl_fat.config(text="")

        ini = ent_ini.get().strip()
        fim = ent_fim.get().strip()

        ok, msg = val.validar_periodo(ini, fim)
        if not ok:
            ui.mensagem_erro(msg)
            return

        produtos_map = {p["id_produto"]: p for p in arq.ler_produtos()}
        pedidos = [p for p in arq.ler_pedidos() if val.data_no_periodo(p["data"], ini, fim)]

        if not pedidos:
            ui.mensagem_aviso("Nenhum pedido encontrado no período informado.")
            return

        total = 0.0
        for p in pedidos:
            prod = produtos_map.get(p["id_produto"], {})
            desc = prod.get("descricao", f"ID {p['id_produto']}")
            vt = float(p["valor_total"])
            total += vt
            tree.insert("", "end",values=(p["data"], p["mesa"], desc, p["qtd"], f"R$ {vt:.2f}".replace(".", ",")))

        lbl_fat.config(text=f"FATURAMENTO DO PERÍODO:  R$ {total:.2f}".replace(".", ","))

    from sistema import renderizar_menu_principal

    fr_btn = tk.Frame(frame, bg=ui.COR_FUNDO)
    fr_btn.pack(pady=4)
    ui.botao_acao(fr_btn, "📊  Gerar", gerar, cor="#313244").pack(side="left", padx=6)
    ui.botao_acao(fr_btn, "✖  Fechar", lambda: renderizar_menu_principal(container), cor="#45475a").pack(side="left", padx=6)

#  RELATÓRIO 2 — Faturamento por tipo de produto

def _relatorio_por_tipo(container: tk.Frame):
    ui.limpar_container(container)

    tk.Label(container, text="SUBMENU: RELATÓRIOS", font=ui.FONTE_TITULO, bg=ui.COR_FUNDO, fg=ui.COR_TITULO).pack(pady=(0, 14))

    frame = ui.frame_conteudo(container)

    fr_datas = tk.Frame(frame, bg=ui.COR_FUNDO)
    fr_datas.pack(fill="x", pady=(0, 4))

    tk.Label(fr_datas, text="Data Inicial:", font=ui.FONTE_NORMAL, bg=ui.COR_FUNDO, fg=ui.COR_TEXTO).grid(row=0, column=0, sticky="w", padx=(0, 4))
    ent_ini = ui.entrada_campo(fr_datas, 12)
    ent_ini.grid(row=0, column=1, padx=(0, 12))

    tk.Label(fr_datas, text="Data Final:", font=ui.FONTE_NORMAL, bg=ui.COR_FUNDO, fg=ui.COR_TEXTO).grid(row=0, column=2, sticky="w", padx=(0, 4))
    ent_fim = ui.entrada_campo(fr_datas, 12)
    ent_fim.grid(row=0, column=3, padx=(0, 12))

    # Combobox de tipo
    tk.Label(fr_datas, text="Tipo:", font=ui.FONTE_NORMAL, bg=ui.COR_FUNDO, fg=ui.COR_TEXTO).grid(row=0, column=4, sticky="w", padx=(0, 4))
    combo_tipo = ttk.Combobox(fr_datas, values=["Todos", "Bebida", "Lanche"], width=8, state="readonly", font=ui.FONTE_NORMAL)
    combo_tipo.current(0)
    combo_tipo.grid(row=0, column=5)

    ui.separador(frame)

    colunas = [("data", "Data", 100), ("mesa", "Mesa", 60), ("tipo", "Tipo", 80), ("desc", "Produto", 200), ("qtd", "Qtd", 50), ("total", "V. Total", 100)]
    fr_tree = tk.Frame(frame, bg=ui.COR_FUNDO)
    fr_tree.pack(fill="both", expand=True)
    tree = ui.criar_treeview(fr_tree, colunas, altura=11)

    ui.separador(frame)

    fr_totais = tk.Frame(frame, bg=ui.COR_FUNDO)
    fr_totais.pack(fill="x", padx=10)

    lbl_beb = tk.Label(fr_totais, text="", font=ui.FONTE_NORMAL, bg=ui.COR_FUNDO, fg=ui.COR_SUCESSO)
    lbl_beb.pack(anchor="e")
    lbl_lan = tk.Label(fr_totais, text="", font=ui.FONTE_NORMAL, bg=ui.COR_FUNDO, fg=ui.COR_SUCESSO)
    lbl_lan.pack(anchor="e")
    lbl_tot = tk.Label(fr_totais, text="", font=("Courier New", 12, "bold"), bg=ui.COR_FUNDO, fg=ui.COR_AVISO)
    lbl_tot.pack(anchor="e")

    def gerar():
        for item in tree.get_children():
            tree.delete(item)
        lbl_beb.config(text="")
        lbl_lan.config(text="")
        lbl_tot.config(text="")

        ini = ent_ini.get().strip()
        fim = ent_fim.get().strip()
        tipo_sel = combo_tipo.get()

        ok, msg = val.validar_periodo(ini, fim)
        if not ok:
            ui.mensagem_erro(msg)
            return

        produtos_map = {p["id_produto"]: p for p in arq.ler_produtos()}
        pedidos = [p for p in arq.ler_pedidos() if val.data_no_periodo(p["data"], ini, fim)]

        if tipo_sel == "Bebida":
            pedidos = [p for p in pedidos if p["id_tipo_produto"] == "1"]
        elif tipo_sel == "Lanche":
            pedidos = [p for p in pedidos if p["id_tipo_produto"] == "2"]

        if not pedidos:
            ui.mensagem_aviso("Nenhum pedido encontrado para o filtro informado.")
            return

        total_beb = total_lan = 0.0
        for p in pedidos:
            prod = produtos_map.get(p["id_produto"], {})
            desc = prod.get("descricao", f"ID {p['id_produto']}")
            tipo = val.tipo_para_texto(p["id_tipo_produto"])
            vt = float(p["valor_total"])
            if p["id_tipo_produto"] == "1":
                total_beb += vt
            else:
                total_lan += vt
            tree.insert("", "end", values=(p["data"], p["mesa"], tipo, desc, p["qtd"], f"R$ {vt:.2f}".replace(".", ",")))
            
        lbl_beb.config(text=f"Total Bebidas :  R$ {total_beb:.2f}".replace(".", ","))
        lbl_lan.config(text=f"Total Lanches :  R$ {total_lan:.2f}".replace(".", ","))
        lbl_tot.config(text=f"TOTAL GERAL   :  R$ {(total_beb+total_lan):.2f}".replace(".", ","))

    from sistema import renderizar_menu_principal

    fr_btn = tk.Frame(frame, bg=ui.COR_FUNDO)
    fr_btn.pack(pady=4)
    ui.botao_acao(fr_btn, "📊  Gerar", gerar, cor="#313244").pack(side="left", padx=6)
    ui.botao_acao(fr_btn, "✖  Fechar", lambda: renderizar_menu_principal(container), cor="#45475a").pack(side="left", padx=6)
