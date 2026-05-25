# ============================================================
# interface.py - Módulo de Interface Visual (Tkinter)
# Responsável por toda a parte visual do sistema
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox

FONTE_TITULO  = ("Courier New", 15, "bold")
FONTE_NORMAL  = ("Courier New", 12)
FONTE_MENU    = ("Courier New", 13)
FONTE_CABEC   = ("Courier New", 14, "bold")
FONTE_PEQUENA = ("Courier New", 12)

COR_FUNDO     = "#1e1e2e"
COR_PAINEL    = "#2a2a3e"
COR_BORDA     = "#4a4a6a"
COR_TEXTO     = "#cdd6f4"
COR_TITULO    = "#89b4fa"
COR_SUCESSO   = "#a6e3a1"
COR_ERRO      = "#f38ba8"
COR_AVISO     = "#fab387"
COR_BTN       = "#313244"
COR_BTN_HOVER = "#45475a"
COR_DESTAQUE  = "#cba6f7"

def configurar_janela(janela: tk.Tk, titulo: str, largura: int = 700, altura: int = 520):
    """Configura a janela principal do sistema."""
    janela.title(titulo)
    janela.configure(bg=COR_FUNDO)
    janela.resizable(True, True)
    # Centraliza na tela
    janela.update_idletasks()
    x = (janela.winfo_screenwidth()  - largura) // 2
    y = (janela.winfo_screenheight() - altura)  // 2
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

def frame_cabecalho(pai: tk.Widget, texto: str) -> tk.Frame:
    """Cria um frame de cabeçalho estilizado."""
    frame = tk.Frame(pai, bg=COR_PAINEL, pady=8)
    frame.pack(fill="x", padx=10, pady=(10, 0))

    linha_topo = tk.Frame(frame, bg=COR_BORDA, height=2)
    linha_topo.pack(fill="x", padx=5)

    lbl = tk.Label(frame, text=texto, font=FONTE_CABEC, bg=COR_PAINEL, fg=COR_TITULO)
    lbl.pack(pady=4)

    linha_base = tk.Frame(frame, bg=COR_BORDA, height=2)
    linha_base.pack(fill="x", padx=5)

    return frame

def frame_conteudo(pai: tk.Widget) -> tk.Frame:
    """Retorna um frame de conteúdo padrão."""
    frame = tk.Frame(pai, bg=COR_FUNDO)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    return frame

def botao_menu(pai: tk.Widget, texto: str, comando, largura: int = 30) -> tk.Button:
    """Cria um botão de menu estilizado."""
    btn = tk.Button(
        pai, text=texto, font=FONTE_MENU, width=largura, bg=COR_BTN, fg=COR_TEXTO, activebackground=COR_BTN_HOVER,
        activeforeground=COR_TITULO, relief="flat", cursor="hand2", command=comando, pady=6
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=COR_BTN_HOVER))
    btn.bind("<Leave>", lambda e: btn.config(bg=COR_BTN))
    return btn

def botao_acao(pai: tk.Widget, texto: str, comando, cor: str = "#45475a", largura: int = 14) -> tk.Button:
    """Cria um botão de ação menor (confirmar, cancelar etc.)."""
    btn = tk.Button(
        pai, text=texto, font=FONTE_NORMAL, width=largura, bg=cor, fg=COR_TEXTO, activebackground=COR_BTN_HOVER,
        activeforeground=COR_TITULO, relief="flat", cursor="hand2", command=comando, pady=4
    )
    return btn

def label_campo(pai: tk.Widget, texto: str) -> tk.Label:
    """Label para nomear campos de formulário."""
    return tk.Label(pai, text=texto, font=FONTE_NORMAL, bg=COR_FUNDO, fg=COR_TEXTO, anchor="w")

def entrada_campo(pai: tk.Widget, largura: int = 30) -> tk.Entry:
    """Campo de entrada padrão."""
    entrada = tk.Entry(pai, font=FONTE_NORMAL, width=largura, bg=COR_PAINEL, fg=COR_TEXTO, insertbackground=COR_TEXTO, relief="flat", bd=4)
    return entrada

def mensagem_sucesso(texto: str):
    messagebox.showinfo("Sucesso", texto)

def mensagem_erro(texto: str):
    messagebox.showerror("Erro", texto)

def mensagem_aviso(texto: str):
    messagebox.showwarning("Aviso", texto)

def confirmar(texto: str) -> bool:
    return messagebox.askyesno("Confirmação", texto)

def criar_treeview(pai: tk.Widget, colunas, altura: int = 12) -> ttk.Treeview:
    """Cria uma Treeview estilizada.
    colunas: lista de (id, titulo, largura)"""
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Custom.Treeview", background=COR_PAINEL, foreground=COR_TEXTO, rowheight=26, fieldbackground=COR_PAINEL, font=FONTE_NORMAL)
    style.configure("Custom.Treeview.Heading", background=COR_BTN, foreground=COR_TITULO, font=("Courier New", 10, "bold"), relief="flat")
    style.map("Custom.Treeview", background=[("selected", COR_BORDA)], foreground=[("selected", COR_TITULO)])

    ids = [c[0] for c in colunas]
    tree = ttk.Treeview(pai, columns=ids, show="headings", height=altura, style="Custom.Treeview")

    for col_id, col_titulo, col_largura in colunas:
        tree.heading(col_id, text=col_titulo)
        tree.column(col_id, width=col_largura, anchor="center")

    scroll = ttk.Scrollbar(pai, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)

    tree.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")

    return tree

def separador(pai: tk.Widget):
    """Linha horizontal de separação."""
    tk.Frame(pai, bg=COR_BORDA, height=1).pack(fill="x", pady=6)