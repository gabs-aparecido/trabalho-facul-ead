"""
RentSmart — Sistema de Orçamento de Locação
Cliente: R.M Imóveis
Descrição: Aplicação orientada a objetos para cálculo de orçamentos de locação
           (apartamentos, casas e estúdios), parcelamento de taxa contratual
           e exportação da projeção financeira de 12 meses em formato CSV.
"""

from abc import ABC, abstractmethod
import csv
import os


def formatar_moeda(valor: float) -> str:
    """Formata um valor numérico no padrão monetário brasileiro (R$ 1.234,56)."""
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


class Imovel(ABC):
    """Classe base abstrata que representa um imóvel disponível para locação."""

    def __init__(self, categoria: str, valor_base: float) -> None:
        self.categoria = categoria
        self.valor_base = valor_base

    @abstractmethod
    def calcular_adicional_quartos(self) -> float:
        """Retorna o valor adicional referente à quantidade de quartos."""

    @abstractmethod
    def calcular_adicional_garagem(self) -> float:
        """Retorna o valor adicional referente às vagas de garagem/estacionamento."""

    def calcular_subtotal(self) -> float:
        """Calcula o valor bruto mensal antes da aplicação de descontos."""
        return (
            self.valor_base
            + self.calcular_adicional_quartos()
            + self.calcular_adicional_garagem()
        )

    def calcular_desconto(self) -> float:
        """Retorna o valor do desconto comercial aplicável (padrão: R$ 0,00)."""
        return 0.0

    def calcular_aluguel_mensal(self) -> float:
        """Calcula o valor líquido final do aluguel mensal."""
        return round(self.calcular_subtotal() - self.calcular_desconto(), 2)

    @abstractmethod
    def obter_descricao_detalhada(self) -> list[tuple[str, float]]:
        """Retorna uma lista de pares (descrição, valor) detalhando o cálculo."""


class Apartamento(Imovel):
    """Representa um apartamento para locação com suas regras comerciais específicas."""

    VALOR_BASE = 700.00
    ADICIONAL_DOIS_QUARTOS = 200.00
    ADICIONAL_GARAGEM = 300.00
    PERCENTUAL_DESCONTO_SEM_CRIANCAS = 0.05

    def __init__(self, quartos: int, tem_garagem: bool, possui_criancas: bool) -> None:
        super().__init__(categoria="Apartamento", valor_base=self.VALOR_BASE)
        if quartos not in (1, 2):
            raise ValueError("Apartamentos devem possuir 1 ou 2 quartos.")
        self.quartos = quartos
        self.tem_garagem = tem_garagem
        self.possui_criancas = possui_criancas

    def calcular_adicional_quartos(self) -> float:
        return self.ADICIONAL_DOIS_QUARTOS if self.quartos == 2 else 0.0

    def calcular_adicional_garagem(self) -> float:
        return self.ADICIONAL_GARAGEM if self.tem_garagem else 0.0

    def calcular_desconto(self) -> float:
        if not self.possui_criancas:
            return round(
                self.calcular_subtotal() * self.PERCENTUAL_DESCONTO_SEM_CRIANCAS, 2
            )
        return 0.0

    def obter_descricao_detalhada(self) -> list[tuple[str, float]]:
        itens = [
            (f"Aluguel-base ({self.categoria} - 1 quarto)", self.valor_base),
            (
                f"Adicional de quartos ({self.quartos} quarto{'s' if self.quartos > 1 else ''})",
                self.calcular_adicional_quartos(),
            ),
            (
                f"Vaga de garagem ({'Sim' if self.tem_garagem else 'Não'})",
                self.calcular_adicional_garagem(),
            ),
        ]
        desconto = self.calcular_desconto()
        if desconto > 0:
            itens.append(("Desconto comercial (5% - sem crianças)", -desconto))
        else:
            itens.append(("Desconto comercial (não aplicável)", 0.0))
        return itens


class Casa(Imovel):
    """Representa uma casa para locação com suas regras comerciais específicas."""

    VALOR_BASE = 900.00
    ADICIONAL_DOIS_QUARTOS = 250.00
    ADICIONAL_GARAGEM = 300.00

    def __init__(self, quartos: int, tem_garagem: bool) -> None:
        super().__init__(categoria="Casa", valor_base=self.VALOR_BASE)
        if quartos not in (1, 2):
            raise ValueError("Casas devem possuir 1 ou 2 quartos.")
        self.quartos = quartos
        self.tem_garagem = tem_garagem

    def calcular_adicional_quartos(self) -> float:
        return self.ADICIONAL_DOIS_QUARTOS if self.quartos == 2 else 0.0

    def calcular_adicional_garagem(self) -> float:
        return self.ADICIONAL_GARAGEM if self.tem_garagem else 0.0

    def obter_descricao_detalhada(self) -> list[tuple[str, float]]:
        return [
            (f"Aluguel-base ({self.categoria} - 1 quarto)", self.valor_base),
            (
                f"Adicional de quartos ({self.quartos} quarto{'s' if self.quartos > 1 else ''})",
                self.calcular_adicional_quartos(),
            ),
            (
                f"Vaga de garagem ({'Sim' if self.tem_garagem else 'Não'})",
                self.calcular_adicional_garagem(),
            ),
            ("Desconto comercial (não aplicável a casas)", 0.0),
        ]


class Estudio(Imovel):
    """Representa um estúdio para locação com regra própria de estacionamento."""

    VALOR_BASE = 1200.00
    PACOTE_DUAS_VAGAS = 250.00
    VALOR_VAGA_ADICIONAL = 60.00

    def __init__(self, contratar_estacionamento: bool, vagas_adicionais: int = 0) -> None:
        super().__init__(categoria="Estúdio", valor_base=self.VALOR_BASE)
        if vagas_adicionais < 0:
            raise ValueError("A quantidade de vagas adicionais não pode ser negativa.")
        self.contratar_estacionamento = contratar_estacionamento
        self.vagas_adicionais = vagas_adicionais if contratar_estacionamento else 0

    def calcular_adicional_quartos(self) -> float:
        return 0.0

    def calcular_adicional_garagem(self) -> float:
        if not self.contratar_estacionamento:
            return 0.0
        return self.PACOTE_DUAS_VAGAS + (
            self.vagas_adicionais * self.VALOR_VAGA_ADICIONAL
        )

    def obter_descricao_detalhada(self) -> list[tuple[str, float]]:
        total_vagas = (2 + self.vagas_adicionais) if self.contratar_estacionamento else 0
        if self.contratar_estacionamento:
            desc_garagem = (
                f"Estacionamento ({total_vagas} vagas: pacote 2 vagas + "
                f"{self.vagas_adicionais} extra{'s' if self.vagas_adicionais != 1 else ''})"
            )
        else:
            desc_garagem = "Estacionamento (Não contratado)"

        return [
            (f"Aluguel-base ({self.categoria})", self.valor_base),
            (desc_garagem, self.calcular_adicional_garagem()),
            ("Desconto comercial (não aplicável a estúdios)", 0.0),
        ]


class ContratoLocacao:
    """
    Gerencia as condições contratuais, o cálculo da taxa de contrato
    e a projeção de pagamentos para os primeiros 12 meses.
    """

    TAXA_CONTRATUAL = 2000.00
    MAX_PARCELAS = 5
    MESES_PROJECAO = 12

    def __init__(self, imovel: Imovel, parcelas_taxa: int) -> None:
        if not 1 <= parcelas_taxa <= self.MAX_PARCELAS:
            raise ValueError(
                f"A taxa contratual deve ser parcelada entre 1 e {self.MAX_PARCELAS} vezes."
            )
        self.imovel = imovel
        self.parcelas_taxa = parcelas_taxa

    def calcular_parcelas_taxa(self) -> list[float]:
        """Calcula o valor de cada parcela da taxa contratual garantindo soma exata."""
        valor_parcela = round(self.TAXA_CONTRATUAL / self.parcelas_taxa, 2)
        parcelas = [valor_parcela] * self.parcelas_taxa
        diferenca = round(self.TAXA_CONTRATUAL - sum(parcelas), 2)
        parcelas[-1] = round(parcelas[-1] + diferenca, 2)
        return parcelas

    def gerar_projecao_anual(self) -> list[dict[str, float | int]]:
        """Gera a lista com os valores previstos mês a mês durante 12 meses."""
        aluguel_mensal = self.imovel.calcular_aluguel_mensal()
        parcelas = self.calcular_parcelas_taxa()
        projecao = []

        for mes in range(1, self.MESES_PROJECAO + 1):
            valor_taxa_mes = parcelas[mes - 1] if mes <= len(parcelas) else 0.0
            total_mes = round(aluguel_mensal + valor_taxa_mes, 2)
            projecao.append(
                {
                    "mes": mes,
                    "aluguel_mensal": aluguel_mensal,
                    "parcela_taxa_contratual": valor_taxa_mes,
                    "total_previsto_mes": total_mes,
                }
            )
        return projecao

    def exportar_csv(self, caminho_arquivo: str = "projecao_locacao_12_meses.csv") -> str:
        """Exporta a projeção anual de 12 meses para um arquivo CSV."""
        projecao = self.gerar_projecao_anual()
        cabecalhos = [
            "Mes",
            "Aluguel_Mensal_BRL",
            "Parcela_Taxa_Contratual_BRL",
            "Total_Previsto_Mes_BRL",
        ]

        with open(caminho_arquivo, mode="w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(cabecalhos)
            for linha in projecao:
                escritor.writerow(
                    [
                        linha["mes"],
                        f"{linha['aluguel_mensal']:.2f}",
                        f"{linha['parcela_taxa_contratual']:.2f}",
                        f"{linha['total_previsto_mes']:.2f}",
                    ]
                )
        return os.path.abspath(caminho_arquivo)

    def exibir_resumo(self) -> None:
        """Apresenta no terminal o demonstrativo completo e separado do orçamento."""
        aluguel_mensal = self.imovel.calcular_aluguel_mensal()
        parcelas = self.calcular_parcelas_taxa()
        projecao = self.gerar_projecao_anual()
        total_anual = sum(item["total_previsto_mes"] for item in projecao)

        largura = 66
        print("\n" + "=" * largura)
        print("R.M IMÓVEIS — ORÇAMENTO DETALHADO DE LOCAÇÃO (RENTSMART)".center(largura))
        print("=" * largura)

        print("\n[1] COMPOSIÇÃO DO ALUGUEL MENSAL RECORRENTE")
        print("-" * largura)
        for descricao, valor in self.imovel.obter_descricao_detalhada():
            sinal = "-" if valor < 0 else " "
            valor_fmt = f"{sinal}{formatar_moeda(abs(valor))}"
            print(f"  {descricao:<46} {valor_fmt:>16}")
        print("-" * largura)
        print(
            f"  {'VALOR FINAL DO ALUGUEL MENSAL:':<46} "
            f"{formatar_moeda(aluguel_mensal):>16}"
        )

        print("\n[2] TAXA CONTRATUAL (CUSTO ADMINISTRATIVO SEPARADO)")
        print("-" * largura)
        print(
            f"  {'Valor total da taxa de contrato:':<46} "
            f"{formatar_moeda(self.TAXA_CONTRATUAL):>16}"
        )
        print(
            f"  {'Condição de parcelamento escolhida:':<46} "
            f"{f'{self.parcelas_taxa}x sem juros':>16}"
        )
        print(
            f"  {'Valor da parcela (meses 1 a ' + str(self.parcelas_taxa) + '):':<46} "
            f"{formatar_moeda(parcelas[0]):>16}"
        )
        print(
            "  Observação: A taxa contratual não integra o aluguel mensal; "
            f"após a {self.parcelas_taxa}ª parcela,\n  o cliente pagará apenas o aluguel mensal."
        )

        print("\n[3] RESUMO FINANCEIRO DO PRIMEIRO ANO (12 MESES)")
        print("-" * largura)
        print(
            f"  {'Total previsto nos 12 meses (Aluguéis + Taxa):':<46} "
            f"{formatar_moeda(total_anual):>16}"
        )
        print("=" * largura)


class SistemaRentSmart:
    """Controla o fluxo de interação com o atendente/cliente e valida entradas."""

    @staticmethod
    def _ler_opcao_inteira(mensagem: str, opcoes_validas: tuple[int, ...]) -> int:
        while True:
            entrada = input(mensagem).strip()
            if entrada.isdigit() and int(entrada) in opcoes_validas:
                return int(entrada)
            opcoes_str = ", ".join(str(o) for o in opcoes_validas)
            print(f"  [!] Entrada inválida. Escolha uma das opções: {opcoes_str}.")

    @staticmethod
    def _ler_inteiro_nao_negativo(mensagem: str) -> int:
        while True:
            entrada = input(mensagem).strip()
            if entrada.isdigit() and int(entrada) >= 0:
                return int(entrada)
            print("  [!] Entrada inválida. Informe um número inteiro igual ou maior que 0.")

    @staticmethod
    def _ler_sim_nao(mensagem: str) -> bool:
        while True:
            entrada = input(mensagem).strip().upper()
            if entrada in ("S", "SIM"):
                return True
            if entrada in ("N", "NAO", "NÃO"):
                return False
            print("  [!] Entrada inválida. Digite 'S' para Sim ou 'N' para Não.")

    def _coletar_dados_imovel(self) -> Imovel:
        print("\nSelecione a categoria do imóvel desejada:")
        print("  [1] Apartamento (Base: R$ 700,00)")
        print("  [2] Casa        (Base: R$ 900,00)")
        print("  [3] Estúdio     (Base: R$ 1.200,00)")

        categoria = self._ler_opcao_inteira("Opção (1, 2 ou 3): ", (1, 2, 3))

        if categoria == 1:
            quartos = self._ler_opcao_inteira(
                "Quantidade de quartos (1 ou 2): ", (1, 2)
            )
            tem_garagem = self._ler_sim_nao(
                "Deseja incluir vaga de garagem (+ R$ 300,00/mês)? [S/N]: "
            )
            possui_criancas = self._ler_sim_nao(
                "O locatário possui crianças residindo no imóvel? [S/N]: "
            )
            return Apartamento(
                quartos=quartos,
                tem_garagem=tem_garagem,
                possui_criancas=possui_criancas,
            )

        if categoria == 2:
            quartos = self._ler_opcao_inteira(
                "Quantidade de quartos (1 ou 2): ", (1, 2)
            )
            tem_garagem = self._ler_sim_nao(
                "Deseja incluir vaga de garagem (+ R$ 300,00/mês)? [S/N]: "
            )
            return Casa(quartos=quartos, tem_garagem=tem_garagem)

        contratar_estacionamento = self._ler_sim_nao(
            "Deseja contratar o pacote de estacionamento (2 vagas por R$ 250,00/mês)? [S/N]: "
        )
        vagas_adicionais = 0
        if contratar_estacionamento:
            vagas_adicionais = self._ler_inteiro_nao_negativo(
                "Quantas vagas adicionais além das 2 inclusas deseja adicionar (R$ 60,00 cada)? "
            )
        return Estudio(
            contratar_estacionamento=contratar_estacionamento,
            vagas_adicionais=vagas_adicionais,
        )

    def executar(self) -> None:
        print("==================================================================")
        print("       RENTSMART — SISTEMA DE ORÇAMENTO DE LOCAÇÃO (R.M IMÓVEIS)  ")
        print("==================================================================")

        imovel = self._coletar_dados_imovel()
        parcelas = self._ler_opcao_inteira(
            "\nEm quantas parcelas deseja pagar a taxa contratual de R$ 2.000,00 (1 a 5)? ",
            (1, 2, 3, 4, 5),
        )

        contrato = ContratoLocacao(imovel=imovel, parcelas_taxa=parcelas)
        contrato.exibir_resumo()

        caminho_csv = contrato.exportar_csv("projecao_locacao_12_meses.csv")
        print(f"\n[OK] Arquivo CSV com a projeção de 12 meses gerado com sucesso em:")
        print(f"     {caminho_csv}\n")


if __name__ == "__main__":
    app = SistemaRentSmart()
    app.executar()