# ============================================================
# arquivos.py - Módulo de Leitura e Gravacao de Arquivos CSV
# ============================================================

import csv
import os

_BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dados")

ARQUIVO_PRODUTOS = os.path.join(_BASE, "produtos.csv")
ARQUIVO_PEDIDOS  = os.path.join(_BASE, "pedidos.csv")

CABECALHO_PRODUTOS = ["id_produto", "id_tipo_produto", "descricao", "valor"]
CABECALHO_PEDIDOS  = [
    "id_pedido", "data", "mesa", "id_produto", "id_tipo_produto",
    "qtd", "valor_unitario", "valor_total", "status_pedido"
]


def _garantir_pasta():
    os.makedirs(_BASE, exist_ok=True)


def inicializar_arquivos():
    """Cria os arquivos CSV com cabecalho se nao existirem."""
    _garantir_pasta()
    for caminho, cabecalho in [
        (ARQUIVO_PRODUTOS, CABECALHO_PRODUTOS),
        (ARQUIVO_PEDIDOS,  CABECALHO_PEDIDOS),
    ]:
        if not os.path.exists(caminho):
            with open(caminho, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=cabecalho)
                writer.writeheader()


# ---------- PRODUTOS ----------

def ler_produtos():
    """Retorna todos os produtos cadastrados."""
    inicializar_arquivos()
    with open(ARQUIVO_PRODUTOS, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def gravar_produto(produto):
    """Adiciona um produto ao arquivo produtos.csv."""
    inicializar_arquivos()
    with open(ARQUIVO_PRODUTOS, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CABECALHO_PRODUTOS)
        writer.writerow(produto)


def produto_existe(id_produto):
    """Verifica se ja existe um produto com esse id."""
    return any(p["id_produto"] == str(id_produto).strip()
               for p in ler_produtos())


def buscar_produto_por_id(id_produto):
    """Retorna o produto com o id informado, ou None."""
    for p in ler_produtos():
        if p["id_produto"] == str(id_produto).strip():
            return p
    return None


# ---------- PEDIDOS ----------

def ler_pedidos():
    """Retorna todos os pedidos."""
    inicializar_arquivos()
    with open(ARQUIVO_PEDIDOS, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def gravar_pedido(pedido):
    """Adiciona um pedido ao arquivo pedidos.csv."""
    inicializar_arquivos()
    with open(ARQUIVO_PEDIDOS, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CABECALHO_PEDIDOS)
        writer.writerow(pedido)


def proximo_id_pedido():
    """Gera o proximo ID de pedido (auto-incremento simples)."""
    pedidos = ler_pedidos()
    if not pedidos:
        return 1
    return max(int(p["id_pedido"]) for p in pedidos) + 1


def pedidos_abertos_por_mesa(mesa):
    """Retorna pedidos com status 'A' da mesa informada."""
    return [p for p in ler_pedidos()
            if p["mesa"] == str(mesa).strip() and p["status_pedido"] == "A"]


def fechar_mesa(mesa):
    """Altera status de 'A' para 'F' em todos os pedidos abertos da mesa."""
    todos = ler_pedidos()
    for p in todos:
        if p["mesa"] == str(mesa).strip() and p["status_pedido"] == "A":
            p["status_pedido"] = "F"
    with open(ARQUIVO_PEDIDOS, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CABECALHO_PEDIDOS)
        writer.writeheader()
        writer.writerows(todos)
