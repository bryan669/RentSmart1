from decimal import Decimal, ROUND_HALF_UP
from imovel import Imovel

TAXA_CONTRATUAL = Decimal("2000.00")


def moeda(valor: Decimal) -> str:
    """Formata Decimal no padrão brasileiro."""
    valor = Decimal(valor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    texto = f"{valor:,.2f}"
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


class Orcamento:
    def __init__(self, imovel: Imovel, parcelas_contrato: int):
        if not 1 <= parcelas_contrato <= 5:
            raise ValueError("A taxa contratual pode ser dividida em 1 a 5 parcelas.")
        self.__imovel = imovel
        self.__parcelas_contrato = parcelas_contrato

    @property
    def imovel(self):
        return self.__imovel

    @property
    def parcelas_contrato(self):
        return self.__parcelas_contrato

    @property
    def aluguel_mensal(self):
        return self.__imovel.calcular_aluguel()

    @property
    def valor_parcela_contrato(self):
        return (TAXA_CONTRATUAL / self.__parcelas_contrato).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

    def resumo(self):
        print("\n" + "=" * 58)
        print("                 ORÇAMENTO RENTSMART")
        print("=" * 58)
        print(self.__imovel.descricao())
        print("-" * 58)
        for descricao, valor in self.__imovel.detalhes_calculo():
            print(f"{descricao:<42} {moeda(valor):>14}")
        print("-" * 58)
        print(f"{'ALUGUEL MENSAL':<42} {moeda(self.aluguel_mensal):>14}")
        print()
        print(f"Taxa contratual (separada do aluguel): {moeda(TAXA_CONTRATUAL)}")
        print(f"Condição: {self.__parcelas_contrato} parcela(s) de {moeda(self.valor_parcela_contrato)}")
        print(f"Total no primeiro mês: {moeda(self.aluguel_mensal + self.valor_parcela_contrato)}")
        print("=" * 58)
