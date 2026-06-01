# ============================================================
# validacoes.py - Módulo de Validações e Tratamento de Erros
# ============================================================

from datetime import datetime

def validar_inteiro_positivo(valor, nome_campo="Valor"):
    """Valida se o valor é um inteiro positivo maior que zero."""
    try:
        n = int(str(valor).strip())
        if n <= 0:
            return False, "{} deve ser maior que zero.".format(nome_campo)
        return True, ""
    except ValueError:
        return False, "{} deve ser um número inteiro válido.".format(nome_campo)

def validar_float_positivo(valor, nome_campo="Valor"):
    """Valida se o valor é um número decimal positivo."""
    try:
        v = float(str(valor).strip().replace(",", "."))
        if v <= 0:
            return False, "{} deve ser maior que zero.".format(nome_campo)
        return True, ""
    except ValueError:
        return False, "{} deve ser um número válido (ex: 12.50).".format(nome_campo)

def validar_descricao(texto):
    """Valida que a descrição não está vazia."""
    if not str(texto).strip():
        return False, "A descricao nao pode estar vazia."
    if len(str(texto).strip()) < 2:
        return False, "A descricao deve ter ao menos 2 caracteres."
    return True, ""

def validar_tipo_produto(tipo):
    """Valida que o tipo de produto é 1 (Bebida) ou 2 (Lanche)."""
    if str(tipo) not in ("1", "2"):
        return False, "Tipo de produto deve ser 1 (Bebida) ou 2 (Lanche)."
    return True, ""

def validar_data(data):
    """Valida o formato de data DD/MM/AAAA."""
    data = str(data).strip()
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True, ""
    except ValueError:
        return False, "Data invalida: '{}'. Use o formato DD/MM/AAAA.".format(data)

def validar_periodo(data_ini, data_fim):
    """Valida que data inicial nao e maior que data final."""
    ok_ini, msg = validar_data(data_ini)
    if not ok_ini:
        return False, "Data inicial - " + msg
    ok_fim, msg = validar_data(data_fim)
    if not ok_fim:
        return False, "Data final - " + msg

    d_ini = datetime.strptime(str(data_ini).strip(), "%d/%m/%Y")
    d_fim = datetime.strptime(str(data_fim).strip(), "%d/%m/%Y")
    if d_ini > d_fim:
        return False, "A data inicial nao pode ser maior que a data final."
    return True, ""

def data_no_periodo(data_pedido, data_ini, data_fim):
    """Retorna True se data_pedido estiver dentro do periodo [ini, fim]."""
    try:
        dp = datetime.strptime(str(data_pedido).strip(), "%d/%m/%Y")
        ini = datetime.strptime(str(data_ini).strip(), "%d/%m/%Y")
        fim = datetime.strptime(str(data_fim).strip(), "%d/%m/%Y")
        return ini <= dp <= fim
    except ValueError:
        return False

def tipo_para_texto(id_tipo):
    """Converte id_tipo_produto para texto legivel."""
    return "Bebida" if str(id_tipo).strip() == "1" else "Lanche"
