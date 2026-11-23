from abc import ABC, abstractmethod
from decimal import Decimal


class Imovel(ABC):
    """Classe-base dos imóveis. Define o contrato comum de cálculo."""

    def __init__(self, aluguel_base: Decimal):
        self.__aluguel_base = Decimal(aluguel_base)

    @property
    def aluguel_base(self) -> Decimal:
        return self.__aluguel_base

    @abstractmethod
    def calcular_aluguel(self) -> Decimal:
        """Retorna o aluguel mensal com adicionais e descontos."""
        raise NotImplementedError

    @abstractmethod
    def descricao(self) -> str:
        raise NotImplementedError

    def detalhes_calculo(self) -> list[tuple[str, Decimal]]:
        """Itens que compõem o aluguel, usados no resumo do orçamento."""
        return [("Aluguel-base", self.aluguel_base)]


class Apartamento(Imovel):
    def __init__(self, quartos: int, garagem: bool, possui_criancas: bool):
        if quartos not in (1, 2):
            raise ValueError("Apartamento deve possuir 1 ou 2 quartos.")

        base = Decimal("700.00") if quartos == 1 else Decimal("700.00")
        super().__init__(base)
        self.__quartos = quartos
        self.__garagem = garagem
        self.__possui_criancas = possui_criancas

    def detalhes_calculo(self):
        itens = [("Aluguel-base", self.aluguel_base)]
        if self.__quartos == 2:
            itens.append(("Adicional por segundo quarto", Decimal("200.00")))
        if self.__garagem:
            itens.append(("Vaga de garagem", Decimal("300.00")))
        subtotal = sum((valor for _, valor in itens), Decimal("0.00"))
        if not self.__possui_criancas:
            itens.append(("Desconto de 5% (apartamento sem crianças)", -(subtotal * Decimal("0.05"))))
        return itens

    def calcular_aluguel(self):
        return sum((valor for _, valor in self.detalhes_calculo()), Decimal("0.00"))

    def descricao(self):
        return f"Apartamento - {self.__quartos} quarto(s), garagem: {'sim' if self.__garagem else 'não'}, crianças: {'sim' if self.__possui_criancas else 'não'}"


class Casa(Imovel):
    def __init__(self, quartos: int, garagem: bool):
        if quartos not in (1, 2):
            raise ValueError("Casa deve possuir 1 ou 2 quartos.")
        super().__init__(Decimal("900.00"))
        self.__quartos = quartos
        self.__garagem = garagem

    def detalhes_calculo(self):
        itens = [("Aluguel-base", self.aluguel_base)]
        if self.__quartos == 2:
            itens.append(("Adicional por segundo quarto", Decimal("250.00")))
        if self.__garagem:
            itens.append(("Vaga de garagem", Decimal("300.00")))
        return itens

    def calcular_aluguel(self):
        return sum((valor for _, valor in self.detalhes_calculo()), Decimal("0.00"))

    def descricao(self):
        return f"Casa - {self.__quartos} quarto(s), garagem: {'sim' if self.__garagem else 'não'}"


class Estudio(Imovel):
    def __init__(self, vagas: int):
        if vagas < 2:
            raise ValueError("O pacote inicial do estúdio inclui no mínimo 2 vagas.")
        super().__init__(Decimal("1200.00"))
        self.__vagas = vagas

    def detalhes_calculo(self):
        itens = [
            ("Aluguel-base", self.aluguel_base),
            ("Pacote inicial de 2 vagas", Decimal("250.00"))
        ]
        vagas_extras = self.__vagas - 2
        if vagas_extras:
            itens.append((f"{vagas_extras} vaga(s) adicional(is)", Decimal("60.00") * vagas_extras))
        return itens

    def calcular_aluguel(self):
        return sum((valor for _, valor in self.detalhes_calculo()), Decimal("0.00"))

    def descricao(self):
        return f"Estúdio - {self.__vagas} vaga(s) no total"
