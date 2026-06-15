import tkinter as tk
from tkinter import ttk
from lib import interface as ui
from lib import validacoes as val
from lib import arquivos as arq

def abrir_menu_produto(container: tk.Frame):
    """Abre a janela do submenu Produto."""
    ui.limpar_container(container)

    tk.Label(container, text="PRODUTOS", font=ui.FONTE_TITULO, bg=ui.COR_FUNDO, fg=ui.COR_TITULO).pack(pady=(0, 14))

    frame = ui.frame_conteudo(container)
    frame.pack_configure(anchor="center")

    from sistema import renderizar_menu_principal

    opcoes = [
        ("1 - Cadastro de Produto", lambda: _abrir_cadastro(container)),
        ("2 - Listagem de Produto", lambda: _abrir_listagem(container)),
        ("3 - Voltar ao Menu Principal", lambda: renderizar_menu_principal(container))]
    for texto, cmd in opcoes:
        btn = ui.botao_menu(frame, texto, cmd)
        btn.pack(pady=5)

#  --------------------CADASTRO----------------------------

def _abrir_cadastro(container: tk.Frame):
    ui.limpar_container(container)
    ui.frame_cabecalho(container, "⬛  CADASTRO DE PRODUTO")

    frame = ui.frame_conteudo(container)

    campos = {}
    rotulos = [("id", "ID do Produto:"), ("tipo", "Tipo  [ 1-Bebida / 2-Lanche ]:"), ("desc", "Descrição:"), ("valor", "Valor Unitário (R$):")]

    for chave, rotulo in rotulos:
        ui.label_campo(frame, rotulo).pack(expand=False, pady=5)
        entrada = ui.entrada_campo(frame, largura=40)
        entrada.pack(expand=False, pady=0)
        campos[chave] = entrada

    ui.separador(frame)

    def salvar():
        id_p = campos["id"].get().strip()
        tipo = campos["tipo"].get().strip()
        desc = campos["desc"].get().strip()
        valor = campos["valor"].get().strip().replace(",", ".")

        # Validações
        ok, msg = val.validar_inteiro_positivo(id_p, "ID do produto")
        if not ok:
            ui.mensagem_erro(msg)
            return

        if arq.produto_existe(id_p):
            ui.mensagem_erro(f"Já existe um produto com ID {id_p}.")
            return

        ok, msg = val.validar_tipo_produto(tipo)
        if not ok:
            ui.mensagem_erro(msg)
            return

        ok, msg = val.validar_descricao(desc)
        if not ok:
            ui.mensagem_erro(msg)
            return

        ok, msg = val.validar_float_positivo(valor, "Valor unitário")
        if not ok:
            ui.mensagem_erro(msg)
            return

        produto = {"id_produto": id_p, "id_tipo_produto": tipo, "descricao": desc, "valor": f"{float(valor):.2f}"}
        arq.gravar_produto(produto)
        ui.mensagem_sucesso(f"Produto '{desc}' cadastrado com sucesso!")

        for e in campos.values():
            e.delete(0, tk.END)
        campos["id"].focus()

    fr_btn = tk.Frame(frame, bg=ui.COR_FUNDO)
    fr_btn.pack(side="bottom", pady=4)
    ui.botao_acao(fr_btn, "\uf0c7 Salvar", salvar, bg="#1D772A", hover_bg="#329C42").pack(side="left", padx=6)

    from sistema import renderizar_menu_principal

    ui.botao_acao(fr_btn, "\uf00d Fechar", lambda: renderizar_menu_principal(container), bg="#45475a").pack(side="left", padx=6)

#  -----------------------LISTAGEM--------------------------

def _abrir_listagem(container: tk.Frame):
    ui.limpar_container(container)
    ui.frame_cabecalho(container, "⬛  LISTAGEM DE PRODUTOS")

    frame = ui.frame_conteudo(container)

    colunas = [("id", "ID", 60), ("tipo", "Tipo", 100), ("desc", "Descrição", 280), ("valor", "Valor Unit.", 110)]
    fr_tree = tk.Frame(frame, bg=ui.COR_FUNDO)
    fr_tree.pack(fill="both", expand=True)
    tree = ui.criar_treeview(fr_tree, colunas, altura=14)

    produtos = arq.ler_produtos()
    if not produtos:
        ui.mensagem_aviso("Nenhum produto cadastrado ainda.")
    else:
        for p in produtos:
            tipo_txt = val.tipo_para_texto(p["id_tipo_produto"])
            valor_fmt = f"R$ {float(p['valor']):.2f}".replace(".", ",")
            tree.insert("", "end", values=(p["id_produto"], tipo_txt, p["descricao"], valor_fmt))

    ui.separador(frame)
    from sistema import renderizar_menu_principal

    ui.botao_acao(frame, "\uf00d Fechar", lambda: renderizar_menu_principal(container)).pack()
