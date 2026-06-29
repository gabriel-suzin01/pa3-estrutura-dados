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
    ui.frame_cabecalho(container, "CADASTRO DE PRODUTO")

    frame = ui.frame_conteudo(container)

    campos = {}
    rotulos = [
        ("tipo", "Tipo:"),
        ("desc", "Nome:"),
        ("valor", "Valor Unitário (R$):"),
    ]

    for chave, rotulo in rotulos:
        ui.label_campo(frame, rotulo).pack(expand=False, pady=5)

        if chave == "tipo":
            entrada = ui.entrada_combobox(frame, valores=["Bebida", "Lanche"], largura=53)
        else:
            entrada = ui.entrada_campo(frame, largura=40)
        entrada.pack(expand=False, pady=0)
        campos[chave] = entrada

    ui.separador(frame)

    def salvar():
        tipo = campos["tipo"].get().strip()
        desc = campos["desc"].get().strip()
        valor = campos["valor"].get().strip().replace(",", ".")

        # Validações

        ok, msg = val.validar_tipo_produto(tipo)
        if not ok:
            ui.mensagem_erro(msg)
            return
        
        conversao_tipo = "1" if tipo.lower() == "bebida" else "2"

        ok, msg = val.validar_descricao(desc)
        if not ok:
            ui.mensagem_erro(msg)
            return

        ok, msg = val.validar_float_positivo(valor, "Valor unitário")
        if not ok:
            ui.mensagem_erro(msg)
            return
        
        produtos = arq.ler_produtos()

        id_produto = 0
        if produtos:
            for p in produtos:
                novo_id = int(p.get("id_produto", 0))
                if novo_id > id_produto:
                    id_produto = novo_id

        produto = {
            "id_produto": id_produto + 1,
            "id_tipo_produto": conversao_tipo,
            "descricao": desc,
            "valor": f"{float(valor):.2f}",
        }
        arq.gravar_produto(produto)
        ui.mensagem_sucesso(f"Produto '{desc}' cadastrado com sucesso!")

        for e in campos.values():
            e.delete(0, tk.END)
        campos["tipo"].focus()

    fr_btn = tk.Frame(frame, bg=ui.COR_FUNDO)
    fr_btn.pack(side="bottom", pady=4)
    ui.botao_acao(fr_btn, "💾 Salvar", salvar, bg="#1D772A", hover_bg="#329C42").pack(side="left", padx=6)

    from sistema import renderizar_menu_principal

    ui.botao_acao(fr_btn, "⬅️ VOLTAR", lambda: renderizar_menu_principal(container), bg="#45475a").pack(side="left", padx=6)

#  -----------------------LISTAGEM--------------------------

def _abrir_listagem(container: tk.Frame):
    ui.limpar_container(container)
    ui.frame_cabecalho(container, "LISTAGEM DE PRODUTOS")

    frame = ui.frame_conteudo(container)

    colunas = [("id", "ID", 60), ("tipo", "Tipo", 100), ("desc", "Descrição", 280), ("valor", "Valor Unit.", 110)]
    fr_tree = tk.Frame(frame, bg=ui.COR_FUNDO)
    fr_tree.pack(fill="both", expand=True)
    tree = ui.criar_treeview(fr_tree, colunas, altura=14)

    produto_selecionado = None

    def ao_selecionar(event):
        btn_remover.config(state="normal")

    tree.bind("<<TreeviewSelect>>", ao_selecionar)

    ui.separador(frame)

    from sistema import renderizar_menu_principal

    btn_frame = tk.Frame(frame, bg=ui.COR_FUNDO)
    btn_frame.pack(pady=6)

    btn_remover = ui.botao_acao(btn_frame, "❌ REMOVER", lambda: _executar_delecao(tree, btn_remover))
    btn_remover.pack(side="left", padx=6)
    btn_remover.config(state="disabled")

    ui.botao_acao(btn_frame, "⬅️ VOLTAR", lambda: renderizar_menu_principal(container)).pack()

    preencher_tabela(tree, btn_remover)

def preencher_tabela(tree, btn_remover):
    """Busca produtos e preenche a tabela."""

    for item in tree.get_children():
        tree.delete(item)

    produtos = {p.get("id_produto"): p for p in arq.ler_produtos()}

    for id, produto in produtos.items():
        tipo_txt = val.tipo_para_texto(produto["id_tipo_produto"])
        valor_fmt = f"R$ {float(produto.get("valor")):.2f}".replace(".", ",")
        tree.insert("", "end", values=(produto.get("id_produto"), tipo_txt, produto["descricao"], valor_fmt))

    btn_remover.config(state="disabled")

def _executar_delecao(tree, btn_remover):
    """Confirma exclusão do produto."""

    selecionados = tree.selection()

    if not selecionados:
        ui.mensagem_aviso("Selecione um produto para fechar.")
        return
    if not tree.get_children():
        return
    
    id_produto = tree.item(selecionados[0], "values")[0]

    if not id_produto:
        ui.mensagem_erro("ID não encontrado!")
        return
    
    produto = arq.buscar_produto_por_id(id_produto)

    if not ui.confirmar(f"Deseja realmente excluir o produto {produto.get("descricao", f"ID #{id_produto}")}?\n"):
        return
    
    arq.remover_produto(id_produto)
    ui.mensagem_sucesso(f"Produto {produto.get("descricao", f"ID #{id_produto}")} excluído com sucesso!")
    preencher_tabela(tree, btn_remover)