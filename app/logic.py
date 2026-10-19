from decimal import Decimal, ROUND_HALF_UP
from typing import Any

CENT = Decimal("0.01")
LIMITE_APROVACAO = Decimal("5000.00")


def processar_solicitacao(data: dict[str, Any]) -> dict[str, Any]:
    """Valida e consolida uma solicitação; não realiza compra nem pagamento."""
    if not isinstance(data, dict):
        raise ValueError("O corpo deve ser um objeto JSON.")
    sid, solicitante, itens = data.get("solicitacao_id"), data.get("solicitante"), data.get("itens")
    if not isinstance(sid, str) or not sid.strip() or len(sid) > 100:
        raise ValueError("solicitacao_id deve ser texto de 1 a 100 caracteres.")
    if not isinstance(solicitante, str) or not solicitante.strip() or len(solicitante) > 200:
        raise ValueError("solicitante deve ser texto de 1 a 200 caracteres.")
    if not isinstance(itens, list) or not 1 <= len(itens) <= 500:
        raise ValueError("itens deve conter de 1 a 500 itens.")

    itens_processados = []
    total = Decimal("0.00")
    for idx, item in enumerate(itens, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"O item {idx} deve ser um objeto.")
        descricao = item.get("descricao")
        quantidade = item.get("quantidade")
        valor = item.get("valor_unitario")
        if not isinstance(descricao, str) or not descricao.strip() or len(descricao) > 200:
            raise ValueError(f"A descrição do item {idx} é inválida.")
        if isinstance(quantidade, bool) or not isinstance(quantidade, int) or not 1 <= quantidade <= 10000:
            raise ValueError(f"A quantidade do item {idx} deve ser um inteiro entre 1 e 10000.")
        try:
            unitario = Decimal(str(valor))
        except Exception as exc:
            raise ValueError(f"O valor unitário do item {idx} é inválido.") from exc
        if not unitario.is_finite() or unitario < 0 or unitario > Decimal("100000000"):
            raise ValueError(f"O valor unitário do item {idx} deve estar entre 0 e 100000000.")
        unitario = unitario.quantize(CENT, rounding=ROUND_HALF_UP)
        subtotal = (unitario * quantidade).quantize(CENT, rounding=ROUND_HALF_UP)
        total += subtotal
        itens_processados.append({"descricao": descricao.strip(), "quantidade": quantidade,
                                  "valor_unitario": float(unitario), "subtotal": float(subtotal)})

    total = total.quantize(CENT, rounding=ROUND_HALF_UP)
    dentro_limite = total <= LIMITE_APROVACAO
    return {"status": "processado", "solicitacao_id": sid.strip(), "solicitante": solicitante.strip(),
            "itens": itens_processados, "total": float(total),
            "decisao": "aprovacao_automatica" if dentro_limite else "revisao_manual",
            "observacao": "Dentro do limite configurado; encaminhar conforme política interna." if dentro_limite
            else f"Total acima do limite de R$ {LIMITE_APROVACAO:.2f}; requer revisão humana."}
