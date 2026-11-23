import csv
from pathlib import Path
from decimal import Decimal
from orcamento import TAXA_CONTRATUAL, moeda


def gerar_projecao_csv(orcamento, caminho="arquivos/projecao_locacao.csv"):
    """Gera a previsão dos 12 meses, incluindo a taxa apenas nas parcelas escolhidas."""
    destino = Path(caminho)
    destino.parent.mkdir(parents=True, exist_ok=True)

    aluguel = orcamento.aluguel_mensal
    parcela = orcamento.valor_parcela_contrato
    quantidade = orcamento.parcelas_contrato

    with destino.open("w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow([
            "Mes", "Aluguel mensal (R$)", "Parcela contratual (R$)",
            "Total previsto no mes (R$)"
        ])

        for mes in range(1, 13):
            taxa_mes = parcela if mes <= quantidade else Decimal("0.00")
            total = aluguel + taxa_mes
            escritor.writerow([
                mes,
                f"{aluguel:.2f}".replace(".", ","),
                f"{taxa_mes:.2f}".replace(".", ","),
                f"{total:.2f}".replace(".", ",")
            ])

    return destino
