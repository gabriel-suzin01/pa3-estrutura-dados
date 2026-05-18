# ============================================================
# fechamento.py - Módulo de Fechamento de Mesa
# ============================================================

import tkinter as tk

from lib import interface as ui
from lib import validacoes as val
from lib import arquivos   as arq


def abrir_fechamento_mesa(janela_pai: tk.Widget):
    """Abre a tela de fechamento de mesa."""
    win = tk.Toplevel(janela_pai)
    ui.configurar_janela(win, "Fechamento de Mesa", 600, 480)
    ui.frame_cabecalho(win, "⬛  FECHAMENTO DE MESA")

    frame = ui.frame_conteudo(win)

    # ── Entrada da mesa ──
    fr_topo = tk.Frame(frame, bg=ui.COR_FUNDO)
    fr_topo.pack(fill="x", pady=(0, 6))

    ui.label_campo(fr_topo, "Número da Mesa:").pack(side="left", padx=(0, 8))
    ent_mesa = ui.entrada_campo(fr_topo, 10)
    ent_mesa.pack(side="left")

    def buscar():
        _preencher_tabela(ent_mesa.get().strip(), frame, tree, lbl_total, btn_fechar)

    ui.botao_acao(fr_topo, "🔍  Buscar", buscar, cor="#313244").pack(side="left", padx=8)

    ui.separador(frame)

    # ── Tabela de itens ──
    colunas = [
        ("desc",   "Produto",       220),
        ("qtd",    "Qtd",            60),
        ("unit",   "V. Unitário",   120),
        ("total",  "V. Total",      120),
    ]
    fr_tree = tk.Frame(frame, bg=ui.COR_FUNDO)
    fr_tree.pack(fill="both", expand=True)
    tree = ui.criar_treeview(fr_tree, colunas, altura=10)

    ui.separador(frame)

    lbl_total = tk.Label(frame, text="", font=("Courier New", 12, "bold"),
                         bg=ui.COR_FUNDO, fg=ui.COR_AVISO)
    lbl_total.pack(anchor="e", padx=10)

    # ── Botões ──
    fr_btn = tk.Frame(frame, bg=ui.COR_FUNDO)
    fr_btn.pack(pady=6)

    btn_fechar = ui.botao_acao(
        fr_btn, "✔  Fechar Mesa",
        lambda: _executar_fechamento(ent_mesa.get().strip(), tree, lbl_total, btn_fechar),
        cor="#313244"
    )
    btn_fechar.pack(side="left", padx=6)
    btn_fechar.config(state="disabled")

    ui.botao_acao(fr_btn, "✖  Sair", win.destroy, cor="#45475a").pack(side="left", padx=6)


def _preencher_tabela(mesa, frame, tree, lbl_total, btn_fechar):
    """Busca pedidos da mesa e preenche a tabela."""
    for item in tree.get_children():
        tree.delete(item)
    lbl_total.config(text="")
    btn_fechar.config(state="disabled")

    ok, msg = val.validar_inteiro_positivo(mesa, "Número da mesa")
    if not ok:
        ui.mensagem_erro(msg); return

    pedidos = arq.pedidos_abertos_por_mesa(mesa)
    if not pedidos:
        ui.mensagem_aviso(f"Mesa {mesa} não possui pedidos em aberto."); return

    # Para exibir a descrição precisamos cruzar com produtos
    produtos_map = {p["id_produto"]: p for p in arq.ler_produtos()}

    total_geral = 0.0
    for p in pedidos:
        prod      = produtos_map.get(p["id_produto"], {})
        desc      = prod.get("descricao", f"ID {p['id_produto']}")
        qtd       = int(p["qtd"])
        val_unit  = float(p["valor_unitario"])
        val_tot   = float(p["valor_total"])
        total_geral += val_tot

        tree.insert("", "end", values=(
            desc, qtd,
            f"R$ {val_unit:.2f}".replace(".", ","),
            f"R$ {val_tot:.2f}".replace(".", ","),
        ))

    lbl_total.config(text=f"TOTAL DA MESA {mesa}:  R$ {total_geral:.2f}".replace(".", ","))
    btn_fechar.config(state="normal")


def _executar_fechamento(mesa, tree, lbl_total, btn_fechar):
    """Confirma e executa o fechamento da mesa."""
    if not tree.get_children():
        return
    if not ui.confirmar(f"Confirmar fechamento da Mesa {mesa}?\nOs pedidos serão marcados como faturados."):
        return
    arq.fechar_mesa(mesa)
    ui.mensagem_sucesso(f"Mesa {mesa} fechada com sucesso!")
    for item in tree.get_children():
        tree.delete(item)
    lbl_total.config(text="")
    btn_fechar.config(state="disabled")
