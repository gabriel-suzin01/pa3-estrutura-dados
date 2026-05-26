# ============================================================
# interface.py - Módulo de Interface Visual (Tkinter)
# Responsável por toda a parte visual do sistema
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox

FONTE_TITULO = ("Courier New", 20, "bold")
FONTE_NORMAL = ("Courier New", 12)
FONTE_MENU = ("Courier New", 15)
FONTE_CABEC = ("Courier New", 17, "bold")
FONTE_PEQUENA = ("Courier New", 12)

COR_FUNDO = "#1e1e2e"
COR_JANELA_PRINCIPALNEL = "#2a2a3e"
COR_BORDA = "#4a4a6a"
COR_TEXTO = "#cdd6f4"
COR_TITULO = "#89b4fa"
COR_SUCESSO = "#a6e3a1"
COR_ERRO = "#f38ba8"
COR_AVISO = "#fab387"
COR_BTN = "#313244"
COR_BTN_HOVER = "#45475a"
COR_DESTAQUE = "#cba6f7"


def configurar_janela(
    titulo: str,
    fullscreen: bool = True,
    largura: int = 700,
    altura: int = 520,
) -> tk.Tk:
    """Configura a janela principal do sistema."""
    janela = tk.Tk()
    janela.title(titulo)
    janela.configure(bg=COR_FUNDO)
    # Centraliza na tela
    janela.update_idletasks()

    if fullscreen:
        janela.attributes("-zoomed", True)
    else:
        janela.resizable(False, False)
        x = (janela.winfo_screenwidth() - largura) // 2
        y = (janela.winfo_screenheight() - altura) // 2
        janela.geometry(f"{largura}x{altura}+{x}+{y}")
    return janela


def frame_cabecalho(container: tk.Widget, texto: str) -> tk.Frame:
    """Cria um frame de cabeçalho estilizado."""
    frame = tk.Frame(container, bg=COR_JANELA_PRINCIPALNEL, pady=8)
    frame.pack(fill="x", padx=10, pady=(10, 0))

    linha_topo = tk.Frame(frame, bg=COR_BORDA, height=2)
    linha_topo.pack(fill="x", padx=5)

    lbl = tk.Label(
        frame, text=texto, font=FONTE_CABEC, bg=COR_JANELA_PRINCIPALNEL, fg=COR_TITULO
    )
    lbl.pack(pady=4)

    linha_base = tk.Frame(frame, bg=COR_BORDA, height=2)
    linha_base.pack(fill="x", padx=5)

    return frame


def frame_conteudo(container: tk.Widget) -> tk.Frame:
    """Retorna um frame de conteúdo padrão."""
    frame = tk.Frame(container, bg=COR_FUNDO)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    return frame


def botao_menu(
    container: tk.Widget, texto: str, comando, largura: int = 30
) -> tk.Button:
    """Cria um botão de menu estilizado."""
    btn = tk.Button(
        container,
        text=texto,
        font=FONTE_MENU,
        width=largura,
        bg=COR_BTN,
        fg=COR_TEXTO,
        activebackground=COR_BTN_HOVER,
        activeforeground=COR_TITULO,
        relief="flat",
        cursor="hand2",
        command=comando,
        pady=6,
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=COR_BTN_HOVER))
    btn.bind("<Leave>", lambda e: btn.config(bg=COR_BTN))
    return btn


def botao_acao(
    container: tk.Widget, texto: str, comando, cor: str = "#45475a", largura: int = 14
) -> tk.Button:
    """Cria um botão de ação menor (confirmar, cancelar etc.)."""
    btn = tk.Button(
        container,
        text=texto,
        font=FONTE_NORMAL,
        width=largura,
        bg=cor,
        fg=COR_TEXTO,
        activebackground=COR_BTN_HOVER,
        activeforeground=COR_TITULO,
        relief="flat",
        cursor="hand2",
        command=comando,
        pady=4,
    )
    return btn


def label_campo(container: tk.Widget, texto: str) -> tk.Label:
    """Label para nomear campos de formulário."""
    return tk.Label(
        container,
        text=texto,
        font=FONTE_NORMAL,
        bg=COR_FUNDO,
        fg=COR_TEXTO,
        anchor="w",
    )


def entrada_campo(container: tk.Widget, largura: int = 30) -> tk.Entry:
    """Campo de entrada padrão."""
    entrada = tk.Entry(
        container,
        font=FONTE_NORMAL,
        width=largura,
        bg=COR_JANELA_PRINCIPALNEL,
        fg=COR_TEXTO,
        insertbackground=COR_TEXTO,
        relief="flat",
        bd=4,
    )
    return entrada


def mensagem_sucesso(texto: str):
    messagebox.showinfo("Sucesso", texto)


def mensagem_erro(texto: str):
    messagebox.showerror("Erro", texto)


def mensagem_aviso(texto: str):
    messagebox.showwarning("Aviso", texto)


def confirmar(texto: str) -> bool:
    return messagebox.askyesno("Confirmação", texto)


def criar_treeview(container: tk.Widget, colunas, altura: int = 12) -> ttk.Treeview:
    """
    Cria uma Treeview estilizada.
    colunas: lista de (id, titulo, largura)
    """
    style = ttk.Style()
    style.theme_use("default")
    style.configure(
        "Custom.Treeview",
        background=COR_JANELA_PRINCIPALNEL,
        foreground=COR_TEXTO,
        rowheight=26,
        fieldbackground=COR_JANELA_PRINCIPALNEL,
        font=FONTE_NORMAL,
    )
    style.configure(
        "Custom.Treeview.Heading",
        background=COR_BTN,
        foreground=COR_TITULO,
        font=("Courier New", 10, "bold"),
        relief="flat",
    )
    style.map(
        "Custom.Treeview",
        background=[("selected", COR_BORDA)],
        foreground=[("selected", COR_TITULO)],
    )

    ids = [c[0] for c in colunas]
    tree = ttk.Treeview(
        container,
        columns=ids,
        show="headings",
        height=altura,
        style="Custom.Treeview",
    )

    for col_id, col_titulo, col_largura in colunas:
        tree.heading(col_id, text=col_titulo)
        tree.column(col_id, width=col_largura, anchor="center")

    scroll = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)

    tree.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")

    return tree


def separador(container: tk.Widget):
    """Linha horizontal de separação."""
    tk.Frame(container, bg=COR_BORDA, height=1).pack(fill="x", pady=6)


def limpar_container(container: tk.Widget):
    """Remove todos os widgets de dentro de um container (geralmente o frame de conteúdo)."""
    for widget in container.winfo_children():
        widget.destroy()
