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

    ui.botao_acao(fr_topo, "🔍  Buscar", buscar, bg="#313244").pack(side="left", padx=8)

    ui.separador(frame)

    # ── Tabela de itens ──
    colunas = [
        ("mesa", "Mesa", 80),
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

    btn_fechar = ui.botao_acao(fr_btn, "❌ Fechar Mesa", lambda: _executar_fechamento(ent_mesa.get().strip(), tree, lbl_total, btn_fechar), bg="#1D772A", hover_bg="#329C42")
    btn_fechar.pack(side="left", padx=6)
    btn_fechar.config(state="disabled")

    from sistema import renderizar_menu_principal

    ui.botao_acao(fr_btn, "\uf00d Sair", lambda: renderizar_menu_principal(container), bg="#45475a").pack(side="left", padx=6)

    # Chama pela primeira vez para renderizar pedidos
    buscar()

def preencher_tabela(mesa, frame, tree, lbl_total, btn_fechar):
    """Busca pedidos da mesa e preenche a tabela."""
    # 1. Limpa a tabela atual
    for item in tree.get_children():
        tree.delete(item)
    lbl_total.config(text="")
    btn_fechar.config(state="disabled")

    # 2. Busca pedidos (se mesa for "", arq.pedidos_abertos_por_mesa retorna todos)
    pedidos = arq.pedidos_abertos_por_mesa(mesa)
    
    if not pedidos:
        msg = f"Mesa {mesa} não possui pedidos em aberto." if mesa else "Não há pedidos em aberto."
        ui.mensagem_aviso(msg)
        return

    # 3. Mapeia produtos para pegar a descrição correta [2]
    produtos_map = {p.get("id_produto"): p for p in arq.ler_produtos()}

    total_geral = 0.0
    for p in pedidos:
        id_ped = p.get("id_pedido", "N/D")
        id_prod = p.get("id_produto", "N/D")
        mesa_id = p.get("mesa", "N/D") # Pega o ID da mesa direto do pedido [1]
        
        # Busca a descrição correta usando o ID do produto
        prod_info = produtos_map.get(id_prod, {})
        desc = prod_info.get("descricao", f"Produto {id_prod}")
        
        qtd = int(p.get("qtd", 0))
        val_unit = float(p.get("valor_unitario", 0))
        val_tot = float(p.get("valor_total", 0))
        total_geral += val_tot

        # 4. INSERÇÃO: Usa mesa_id (do arquivo) em vez da variável mesa (da busca)
        tree.insert("", "end", values=(
            mesa_id, 
            id_ped, 
            desc, 
            qtd, 
            f"R$ {val_unit:.2f}".replace(".", ","), 
            f"R$ {val_tot:.2f}".replace(".", ",")
        ))

    # 5. Atualiza o label de total
    texto_total = f"TOTAL DA MESA {mesa}" if mesa else "TOTAL GERAL EM ABERTO"
    lbl_total.config(text=f"{texto_total}: R$ {total_geral:.2f}".replace(".", ","))
    
    # Só habilita o botão de fechar se uma mesa específica foi digitada
    if mesa:
        btn_fechar.config(state="normal")
    else:
        btn_fechar.config(state="disabled")

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
