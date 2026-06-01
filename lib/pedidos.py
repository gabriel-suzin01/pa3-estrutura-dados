import tkinter as tk
from datetime import datetime

from lib import interface as ui
from lib import validacoes as val
from lib import arquivos as arq
from lib.fechamento import abrir_fechamento_mesa

def abrir_menu_pedidos(container: tk.Frame):
    """Submenu Pedidos — Renderizado limpando o mesmo container."""
    ui.limpar_container(container)

    tk.Label(container, text="SUBMENU: PEDIDOS", font=ui.FONTE_TITULO, bg=ui.COR_FUNDO, fg=ui.COR_TITULO).pack(pady=(0, 14))

    from sistema import renderizar_menu_principal

    opcoes = [
        ("1 - Lançar Pedido", lambda: abrir_lancamento_pedido(container)),
        ("2 - Fechamento de Mesa", lambda: abrir_fechamento_mesa(container)),
        ("3 - Voltar ao Menu Principal",lambda: renderizar_menu_principal(container))]
    
    for texto, cmd in opcoes:
        ui.botao_menu(container, texto, cmd).pack(pady=5)

def abrir_lancamento_pedido(container: tk.Frame):
    """Abre a tela de lançamento de pedido."""
    ui.limpar_container(container)
    ui.frame_cabecalho(container, "⬛  LANÇAR PEDIDO")

    frame = ui.frame_conteudo(container)

    # ── Mesa ──
    ui.label_campo(frame, "Número da Mesa:").pack(anchor="w", pady=(4, 0))
    ent_mesa = ui.entrada_campo(frame, 20)
    ent_mesa.pack(anchor="w")

    ui.separador(frame)

    # ── Tabela de produtos disponíveis ──
    ui.label_campo(frame, "Produtos Disponíveis:").pack(anchor="w", pady=(2, 2))

    colunas = [("id", "ID", 60), ("tipo", "Tipo", 90), ("desc", "Descrição", 240), ("valor", "Valor Unit.", 110)]
    
    fr_tree = tk.Frame(frame, bg=ui.COR_FUNDO)
    fr_tree.pack(fill="x")
    tree = ui.criar_treeview(fr_tree, colunas, altura=7)

    produtos = arq.ler_produtos()
    for p in produtos:
        tipo_txt = val.tipo_para_texto(p["id_tipo_produto"])
        valor_fmt = f"R$ {float(p['valor']):.2f}".replace(".", ",")
        tree.insert("", "end", values=(p["id_produto"], tipo_txt, p["descricao"], valor_fmt))

    ui.separador(frame)

    # ── Seleção do produto e quantidade ──
    fr_sel = tk.Frame(frame, bg=ui.COR_FUNDO)
    fr_sel.pack(fill="x")

    tk.Label(fr_sel, text="ID do Produto:", font=ui.FONTE_NORMAL, bg=ui.COR_FUNDO, fg=ui.COR_TEXTO).grid(row=0, column=0, sticky="w", padx=(0, 8))
    ent_id = ui.entrada_campo(fr_sel, 10)
    ent_id.grid(row=0, column=1, sticky="w")

    tk.Label(fr_sel, text="Quantidade:", font=ui.FONTE_NORMAL, bg=ui.COR_FUNDO, fg=ui.COR_TEXTO).grid(row=0, column=2, sticky="w", padx=(16, 8))
    ent_qtd = ui.entrada_campo(fr_sel, 10)
    ent_qtd.grid(row=0, column=3, sticky="w")

    lbl_total = tk.Label(frame, text="", font=ui.FONTE_NORMAL, bg=ui.COR_FUNDO, fg=ui.COR_SUCESSO)
    lbl_total.pack(anchor="w", pady=(4, 0))

    def confirmar_pedido():
        mesa = ent_mesa.get().strip()
        id_p = ent_id.get().strip()
        qtd_s = ent_qtd.get().strip()

        ok, msg = val.validar_inteiro_positivo(mesa, "Número da mesa")
        if not ok:
            ui.mensagem_erro(msg)
            return

        ok, msg = val.validar_inteiro_positivo(id_p, "ID do produto")
        if not ok:
            ui.mensagem_erro(msg)
            return

        produto = arq.buscar_produto_por_id(id_p)
        if produto is None:
            ui.mensagem_erro(f"Produto ID {id_p} não encontrado.")
            return

        ok, msg = val.validar_inteiro_positivo(qtd_s, "Quantidade")
        if not ok:
            ui.mensagem_erro(msg)
            return

        qtd = int(qtd_s)
        val_unit = float(produto["valor"])
        val_total = qtd * val_unit
        id_pedido = arq.proximo_id_pedido()
        data_hoje = datetime.now().strftime("%d/%m/%Y")

        resumo = (
            f"Mesa: {mesa}\n"
            f"Produto: {produto['descricao']}\n"
            f"Quantidade: {qtd}\n"
            f"Valor unitário: R$ {val_unit:.2f}\n"
            f"Valor total: R$ {val_total:.2f}\n\n"
            "Confirmar lançamento?"
        )
        if not ui.confirmar(resumo):
            return

        pedido = {"id_pedido": id_pedido, "data": data_hoje, "mesa": mesa, "id_produto": produto["id_produto"], "id_tipo_produto": produto["id_tipo_produto"],
                "qtd": qtd, "valor_unitario": f"{val_unit:.2f}", "valor_total": f"{val_total:.2f}", "status_pedido": "A"}
        arq.gravar_pedido(pedido)
        ui.mensagem_sucesso(
            f"Pedido #{id_pedido} lançado!\n"
            f"Mesa {mesa} — {produto['descricao']} x{qtd} = R$ {val_total:.2f}"
        )
        ent_id.delete(0, tk.END)
        ent_qtd.delete(0, tk.END)
        lbl_total.config(text="")

    fr_btn = tk.Frame(frame, bg=ui.COR_FUNDO)
    fr_btn.pack(pady=6)
    ui.botao_acao(fr_btn, "✔  Lançar Pedido", confirmar_pedido, cor="#313244").pack(side="left", padx=6)
    from sistema import renderizar_menu_principal

    ui.botao_acao(fr_btn, "✖  Fechar", lambda: renderizar_menu_principal(container), cor="#45475a").pack(side="left", padx=6)
