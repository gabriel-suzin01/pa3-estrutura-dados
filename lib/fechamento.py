import tkinter as tk
from lib import interface as ui
from lib import validacoes as val
from lib import arquivos as arq

def abrir_fechamento_mesa(container: tk.Frame):
    """Abre a tela de fechamento de mesa."""
    ui.limpar_container(container)

    ui.frame_cabecalho(container, "FECHAMENTO DE MESA")

    frame = ui.frame_conteudo(container)

    # ── Entrada da mesa ──
    fr_topo = tk.Frame(frame, bg=ui.COR_FUNDO)
    fr_topo.pack(fill="x", pady=(0, 6))

    ui.label_campo(fr_topo, "Número da Mesa:").pack(side="left", padx=(0, 8))
    ent_mesa = ui.entrada_campo(fr_topo, 10)
    ent_mesa.pack(side="left")

    def buscar():
        preencher_tabela(ent_mesa.get().strip(), frame, tree, lbl_total, btn_fechar)

    ui.botao_acao(fr_topo, "🔍 BUSCAR", buscar, bg="#313244").pack(side="left", padx=8)

    ui.separador(frame)

    # ── Tabela de itens ──
    colunas = [
        ("mesa", "Mesa", 80),
        ("id", "Numero do Pedido", 60),
        ("desc", "Produto", 220),
        ("qtd", "Quantidade", 60),
        ("unit", "Valor Unitário", 120),
        ("total", "Valor Total", 120)]
    
    fr_tree = tk.Frame(frame, bg=ui.COR_FUNDO)
    fr_tree.pack(fill="both", expand=True)
    tree = ui.criar_treeview(fr_tree, colunas, altura=10)

    mesa_selecionada = {"mesa": None}

    def ao_selecionar(event):
        selecionados = tree.selection()

        if not selecionados:
            return

        item = selecionados[0]
        valores = tree.item(item, "values")

        if not valores:
            return

        mesa = str(valores[0])

        itens_mesa = []

        for iid in tree.get_children():
            vals = tree.item(iid, "values")
            if str(vals[0]) == mesa:
                itens_mesa.append(iid)

        atual = set(tree.selection())
        desejado = set(itens_mesa)

        # evita disparar seleção infinitamente
        if atual != desejado:
            tree.selection_set(itens_mesa)

        mesa_selecionada["mesa"] = mesa
        btn_fechar.config(state="normal")

    tree.bind("<<TreeviewSelect>>", ao_selecionar)

    ui.separador(frame)

    lbl_total = tk.Label(frame, text="", font=("Courier New", 12, "bold"), bg=ui.COR_FUNDO, fg=ui.COR_AVISO)
    lbl_total.pack(anchor="e", padx=10)

    # ── Botões ──
    fr_btn = tk.Frame(frame, bg=ui.COR_FUNDO)
    fr_btn.pack(pady=6)

    btn_fechar = ui.botao_acao(
        fr_btn,
        "❌ Fechar Mesa",
        lambda: _executar_fechamento(
            mesa_selecionada["mesa"],
            tree,
            lbl_total,
            btn_fechar
        ),
        bg="#1D772A",
        hover_bg="#329C42"
    )
    btn_fechar.pack(side="left", padx=6)
    btn_fechar.config(state="disabled")

    from sistema import renderizar_menu_principal

    ui.botao_acao(fr_btn, "⬅️ VOLTAR", lambda: renderizar_menu_principal(container), bg="#45475a").pack(side="left", padx=6)

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
        msg = f"Mesa {mesa} não possui pedidos em aberto." if mesa else "Não há pedidos em aberto."
        ui.mensagem_aviso(msg)
        return

    produtos_map = {p.get("id_produto"): p for p in arq.ler_produtos()}

    total_geral = 0.0
    for p in pedidos:
        id_ped = p.get("id_pedido", "N/D")
        id_prod = p.get("id_produto", "N/D")
        mesa_id = p.get("mesa", "N/D")
        
        prod_info = produtos_map.get(id_prod, {})
        desc = prod_info.get("descricao", f"Produto {id_prod}")
        
        qtd = int(p.get("qtd", 0))
        val_unit = float(p.get("valor_unitario", 0))
        val_tot = float(p.get("valor_total", 0))
        total_geral += val_tot

        tree.insert("", "end", values=(
            mesa_id, 
            id_ped, 
            desc, 
            qtd, 
            f"R$ {val_unit:.2f}".replace(".", ","), 
            f"R$ {val_tot:.2f}".replace(".", ",")
        ))

    texto_total = f"TOTAL DA MESA {mesa}" if mesa else "TOTAL GERAL EM ABERTO"
    lbl_total.config(text=f"{texto_total}: R$ {total_geral:.2f}".replace(".", ","))
    
    btn_fechar.config(state="disabled")

def _executar_fechamento(mesa, tree, lbl_total, btn_fechar):
    """Confirma e executa o fechamento da mesa."""
    if not mesa:
        ui.mensagem_aviso("Selecione uma mesa para fechar.")
        return
    if not tree.get_children():
        return
    if not ui.confirmar(f"Confirmar fechamento da Mesa {mesa}?\nOs pedidos serão marcados como faturados."):
        return
    arq.fechar_mesa(mesa)
    ui.mensagem_sucesso(f"Mesa {mesa} fechada com sucesso!")
    preencher_tabela("", None, tree, lbl_total, btn_fechar)
