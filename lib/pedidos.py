import tkinter as tk
from datetime import datetime

from lib import interface as ui
from lib import validacoes as val
from lib import arquivos as arq
from lib.fechamento import abrir_fechamento_mesa

def abrir_menu_pedidos(container: tk.Frame):
    """Submenu Pedidos — Renderizado limpando o mesmo container."""
    ui.limpar_container(container)

    tk.Label(container, text="PEDIDOS", font=ui.FONTE_TITULO, bg=ui.COR_FUNDO, fg=ui.COR_TITULO).pack(pady=(0, 14))

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
    ui.frame_cabecalho(container, "LANÇAR PEDIDO")

    frame = ui.frame_conteudo(container)

    campos = {}
    rotulos = [
        ("mesa", "Número da Mesa:"),
        ("descricao", "Produto:"),
        ("qtd", "Quantidade:")
    ]

    # ── Seleção do produto e quantidade ──
    fr_sel = tk.Frame(frame, bg=ui.COR_FUNDO)
    fr_sel.pack(fill="x")

    for chave, rotulo in rotulos:
        ui.label_campo(frame, rotulo).pack(expand=False, pady=5)

        if chave == "descricao":
            entrada = ui.entrada_combobox(frame, valores=[f"({p.get("id_produto")}) - {p.get("descricao")}" for p in arq.ler_produtos()], largura=53)
        else:
            entrada = ui.entrada_campo(frame, largura=40)

        entrada.pack(expand=False, pady=0)
        campos[chave] = entrada

    lbl_total = tk.Label(frame, text="", font=ui.FONTE_NORMAL, bg=ui.COR_FUNDO, fg=ui.COR_SUCESSO)
    lbl_total.pack(anchor="w", pady=(4, 0))

    def confirmar_pedido():
        import re

        mesa = campos["mesa"].get().strip()

        id_desc_p = campos["descricao"].get().strip()
        match = re.search(r"\((.*?)\)", id_desc_p)

        if match:
            id_p = int(match.group(1))
        else:
            ui.mensagem_erro("ID do produto não foi encontrado!")
            return

        qtd_s = campos["qtd"].get().strip()

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
        campos["id_produto"].delete(0, tk.END)
        campos["qtd"].delete(0, tk.END)
        lbl_total.config(text="")

    fr_btn = tk.Frame(frame, bg=ui.COR_FUNDO)
    fr_btn.pack(side="bottom", pady=6)

    ui.botao_acao(fr_btn, "✔️ LANÇAR PEDIDO", confirmar_pedido, bg="#1D772A", hover_bg="#329C42").pack(side="left", padx=6)

    from sistema import renderizar_menu_principal

    ui.botao_acao(fr_btn, "⬅️ VOLTAR", lambda: renderizar_menu_principal(container), bg="#45475a").pack(side="left", padx=6)
