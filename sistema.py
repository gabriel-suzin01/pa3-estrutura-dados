#!/usr/bin/env python3
# ============================================================
#  sistema.py — Arquivo Principal do Sistema de Pedidos
#  Universidade Alto Vale do Rio do Peixe — UNIARP
#  Estrutura de Dados 3ª Fase / 2026
#  Professor: Emanuel Tonis Florz
# ============================================================

import tkinter as tk
import sys
import os

# Garante que os módulos em lib/ sejam encontrados ao executar
# sistema.py de qualquer diretório
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from lib import interface as ui
from lib import arquivos as arq
from lib.produtos import abrir_menu_produto
from lib.pedidos import abrir_lancamento_pedido
from lib.fechamento import abrir_fechamento_mesa
from lib.relatorios import abrir_menu_relatorios


def abrir_menu_pedidos(janela_pai: tk.Tk):
    """Abre o submenu Pedidos."""
    win = tk.Toplevel(janela_pai)
    ui.configurar_janela(win, "PEDIDOS", 480, 270)
    ui.frame_cabecalho(win, "⬛  PEDIDOS")

    frame = ui.frame_conteudo(win)
    frame.pack_configure(anchor="center")

    opcoes = [
        ("1  -  Lançar Pedido", lambda: abrir_lancamento_pedido(win)),
        ("2  -  Fechamento de Mesa", lambda: abrir_fechamento_mesa(win)),
        ("3  -  Voltar ao Menu Principal", win.destroy),
    ]
    for texto, cmd in opcoes:
        ui.botao_menu(frame, texto, cmd).pack(pady=5)


def iniciar_sistema():
    """Inicializa os arquivos e abre o menu principal."""
    arq.inicializar_arquivos()

    janela = tk.Tk()
    ui.configurar_janela(janela, "Sistema de Pedidos - Choperia", 560, 440)

    # ── Cabeçalho principal ──
    ui.frame_cabecalho(janela, "⬛  SISTEMA DE PEDIDOS  —  BODEGA")

    tk.Label(
        janela,
        text="Estrutura de Dados  |  3ª Fase / 2026  |  Prof. Emanuel Tonis Florz",
        font=ui.FONTE_PEQUENA,
        bg=ui.COR_FUNDO,
        fg=ui.COR_BORDA,
    ).pack(pady=(4, 0))

    ui.separador(janela)

    # ── Menu principal ──
    frame = ui.frame_conteudo(janela)
    frame.pack_configure(anchor="center")

    tk.Label(
        frame,
        text="MENU PRINCIPAL",
        font=ui.FONTE_TITULO,
        bg=ui.COR_FUNDO,
        fg=ui.COR_DESTAQUE,
    ).pack(pady=(0, 14))

    opcoes = [
        ("1  -  Produto", lambda: abrir_menu_produto(janela)),
        ("2  -  Pedidos", lambda: abrir_menu_pedidos(janela)),
        ("3  -  Relatórios", lambda: abrir_menu_relatorios(janela)),
        ("4  -  Sair", janela.destroy),
    ]
    for texto, cmd in opcoes:
        ui.botao_menu(frame, texto, cmd, largura=34).pack(pady=6)

    ui.separador(janela)

    tk.Label(
        janela,
        text="© 2026 UNIARP — Caçador, SC",
        font=ui.FONTE_PEQUENA,
        bg=ui.COR_FUNDO,
        fg=ui.COR_BORDA,
    ).pack(pady=4)

    janela.mainloop()


if __name__ == "__main__":
    iniciar_sistema()
