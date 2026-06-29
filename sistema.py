import os
import sys
import tkinter as tk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from lib import arquivos as arq
from lib import interface as ui
from lib.produtos import abrir_menu_produto
from lib.pedidos import abrir_menu_pedidos
from lib.relatorios import abrir_menu_relatorios

# ── TELAS DO SISTEMA (RODAM NO MESMO CONTAINER) ──
def renderizar_menu_principal(container: tk.Frame):
    """Limpa o container e renderiza o Menu Principal."""
    ui.limpar_container(container)

    tk.Label(container, text="MENU PRINCIPAL DA BODEGA", font=ui.FONTE_TITULO, bg=ui.COR_FUNDO, fg=ui.COR_DESTAQUE).pack(pady=(0, 14))

    opcoes = [
        ("1 - Produto", lambda: abrir_menu_produto(container)),
        ("2 - Pedidos", lambda: abrir_menu_pedidos(container)),
        ("3 - Relatórios", lambda: abrir_menu_relatorios(container)),
        ("4 - Sair", container.quit)
    ]
    
    for texto, cmd in opcoes:
        ui.botao_menu(container, texto, cmd, largura=34).pack(pady=6)

# ── INICIALIZAÇÃO DO SISTEMA ──
def iniciar_sistema():
    """Inicializa os arquivos e monta a estrutura fixa da janela."""
    arq.inicializar_arquivos()

    janela = ui.configurar_janela("Sistema de Pedidos — Bodega")

    # ── Cabeçalho Principal (Fixo no topo da janela) ──
    ui.frame_cabecalho(janela, "BODEGA DOS GURIZES")
    tk.Label(janela, text="Estrutura de Dados  |  3ª Fase / 2026", font=ui.FONTE_PEQUENA, bg=ui.COR_FUNDO, fg=ui.COR_BORDA).pack(pady=(4, 0))
    ui.separador(janela)

    # ── O CONTAINER ÚNICO ──
    # Criamos o frame de conteúdo UMA ÚNICA VEZ aqui.
    # Ele nunca mais será recriado, apenas limpo por dentro.
    frame_conteudo_principal = ui.frame_conteudo(janela)
    frame_conteudo_principal.pack_configure(anchor="center")

    # ── Rodapé (Fixo na base da janela) ──
    ui.separador(janela)
    tk.Label(janela, text="© Felipe, Gabriel, Higor, Humberto e Leonardo — Uniarp Caçador, SC", font=ui.FONTE_PEQUENA, bg=ui.COR_FUNDO, fg=ui.COR_BORDA).pack(pady=4)

    # Inicializa o miolo do sistema passando o container fixo
    renderizar_menu_principal(frame_conteudo_principal)

    janela.mainloop()

if __name__ == "__main__":
    iniciar_sistema()