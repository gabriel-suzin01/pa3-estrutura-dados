import tkinter as tk
from lib import interface as ui
from lib import validacoes as val
from lib import arquivos as arq

def abrir_fechamento_mesa(container: tk.Frame):
    """Abre a tela de fechamento de mesa."""
    ui.limpar_container(container)

    ui.frame_cabecalho(container, "⬛  FECHAMENTO DE MESA")

    frame = ui.frame_conteudo(container)

    # ── Entrada da mesa ──
    fr_topo = tk.Frame(frame, bg=ui.COR_FUNDO)
    fr_topo.pack(fill="x", pady=(0, 6))

    ui.label_campo(fr_topo, "Número da Mesa:").pack(side="left", padx=(0, 8))
    ent_mesa = ui.entrada_campo(fr_topo, 10)
    ent_mesa.pack(side="left")

    def buscar():
        preencher_tabela(ent_mesa.get().strip(), frame, tree, lbl_total, btn_fechar)

    ui.botao_acao(fr_topo, "🔍  Buscar", buscar, cor="#313244").pack(side="left", padx=8)

    ui.separador(frame)

    # ── Tabela de itens ──
    colunas = [
        ("id", "ID.", 60),
        ("desc", "Produto", 220),
        ("qtd", "Qtd.", 60),
        ("unit", "V. Unitário", 120),
        ("total", "V. Total", 120)]
    
    fr_tree = tk.Frame(frame, bg=ui.COR_FUNDO)
    fr_tree.pack(fill="both", expand=True)
    tree = ui.criar_treeview(fr_tree, colunas, altura=10)

    ui.separador(frame)

    lbl_total = tk.Label(frame, text="", font=("Courier New", 12, "bold"), bg=ui.COR_FUNDO, fg=ui.COR_AVISO)
    lbl_total.pack(anchor="e", padx=10)

    # ── Botões ──
    fr_btn = tk.Frame(frame, bg=ui.COR_FUNDO)
    fr_btn.pack(pady=6)

    btn_fechar = ui.botao_acao(fr_btn, "✔  Fechar Mesa", lambda: _executar_fechamento(ent_mesa.get().strip(), tree, lbl_total, btn_fechar), cor="#313244")
    btn_fechar.pack(side="left", padx=6)
    btn_fechar.config(state="disabled")

    from sistema import renderizar_menu_principal

    ui.botao_acao(fr_btn, "✖  Sair", lambda: renderizar_menu_principal(container), cor="#45475a").pack(side="left", padx=6)

    # Chama pela primeira vez para renderizar pedidos
    buscar()

def preencher_tabela(mesa, frame, tree, lbl_total, btn_fechar):
    """Busca pedidos da mesa e preenche a tabela."""
    for item in tree.get_children():
        tree.delete(item)
    lbl_total.config(text="")
    btn_fechar.config(state="disabled")

    pedidos = arq.pedidos_abertos_por_mesa(mesa)
    if not pedidos:
        ui.mensagem_aviso(f"Mesa {mesa} não possui pedidos em aberto.")
        return

    # Para exibir a descrição precisamos cruzar com produtos
    produtos_map = {p.get("id_produto", "N/D"): p for p in arq.ler_produtos()}

    total_geral = 0.0
    for p in pedidos:
        id_ped = p.get("id_pedido", "N/D")
        prod = produtos_map.get(id_ped, {})
        desc = prod.get("descricao", f"ID {p.get("id_produto", "N/D")}")
        qtd = int(p.get("qtd", "N/D"))
        val_unit = float(p.get("valor_unitario", "N/D"))
        val_tot = float(p.get("valor_total", "N/D"))
        total_geral += val_tot

        tree.insert("", "end", values=(id_ped, desc, qtd, f"R$ {val_unit:.2f}".replace(".", ","), f"R$ {val_tot:.2f}".replace(".", ",")))

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
