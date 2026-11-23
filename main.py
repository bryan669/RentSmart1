from imovel import Apartamento, Casa, Estudio
from orcamento import Orcamento, moeda
from gerador_csv import gerar_projecao_csv


def ler_opcao(mensagem, opcoes):
    while True:
        valor = input(mensagem).strip()
        if valor in opcoes:
            return valor
        print(f"Opção inválida. Escolha: {', '.join(opcoes)}.")


def ler_sim_nao(mensagem):
    return ler_opcao(mensagem + " (s/n): ", ["s", "n"]) == "s"


def ler_inteiro(mensagem, minimo, maximo):
    while True:
        try:
            valor = int(input(mensagem))
            if minimo <= valor <= maximo:
                return valor
            print(f"Digite um número entre {minimo} e {maximo}.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def criar_imovel():
    print("\nTIPO DE IMÓVEL")
    print("1 - Apartamento")
    print("2 - Casa")
    print("3 - Estúdio")
    tipo = ler_opcao("Escolha uma opção: ", ["1", "2", "3"])

    if tipo == "1":
        quartos = ler_inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = ler_sim_nao("Deseja vaga de garagem (+ R$ 300,00)?")
        criancas = ler_sim_nao("O cliente possui crianças?")
        return Apartamento(quartos, garagem, criancas)

    if tipo == "2":
        quartos = ler_inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = ler_sim_nao("Deseja vaga de garagem (+ R$ 300,00)?")
        return Casa(quartos, garagem)

    vagas = ler_inteiro("Quantidade total de vagas (mínimo 2): ", 2, 20)
    return Estudio(vagas)


def main():
    print("=" * 58)
    print("             BEM-VINDO AO RENTSMART")
    print("       Sistema de orçamento - R.M Imóveis")
    print("=" * 58)

    imovel = criar_imovel()
    parcelas = ler_inteiro(
        "\nEm quantas parcelas deseja pagar a taxa contratual (1 a 5)? ",
        1, 5
    )

    orcamento = Orcamento(imovel, parcelas)
    orcamento.resumo()

    caminho = gerar_projecao_csv(orcamento)
    print(f"\nProjeção de 12 meses gerada com sucesso: {caminho.resolve()}")
    print("O arquivo separa aluguel, parcela contratual e total mensal.")


if __name__ == "__main__":
    main()
