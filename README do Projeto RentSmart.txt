RentSmart — Sistema de Orçamento de Locação
Aplicação desenvolvida em Python aplicando Pensamento Algorítmico e Programação Orientada a Objetos (POO) para automatizar o cálculo de orçamentos de locação da R.M Imóveis, substituindo processos manuais por uma solução estruturada, validada e capaz de gerar projeções financeiras em CSV.
________________


Regras de Negócio Implementadas
Categoria
	Aluguel-Base
	Adicional de Quartos
	Garagem / Estacionamento
	Desconto Comercial
	Apartamento
	R$ 700,00
	+ R$ 200,00 (2 quartos)
	+ R$ 300,00 (1 vaga opcional)
	5% sobre o aluguel com adicionais caso não possua crianças
	Casa
	R$ 900,00
	+ R$ 250,00 (2 quartos)
	+ R$ 300,00 (1 vaga opcional)
	Não se aplica
	Estúdio
	R$ 1.200,00
	Não se aplica
	Pacote de 2 vagas por R 60,00 por vaga adicional
	Não se aplica
	* Taxa Contratual: Valor fixo de R$ 2.000,00, apresentado separadamente do aluguel mensal e parcelável entre 1 e 5 vezes.
* Projeção Anual: Exportação automática do arquivo projecao_locacao_12_meses.csv contendo os valores previstos mês a mês ao longo dos primeiros 12 meses de contrato.
________________


Estrutura Orientada a Objetos
O sistema foi modelado separando responsabilidades entre domínio imobiliário, regras contratuais e interface de interação:
* Imovel (Classe Abstrata - ABC): Define o contrato comum de precificação (calcular_adicional_quartos, calcular_adicional_garagem, calcular_subtotal, calcular_desconto e calcular_aluguel_mensal).
* Apartamento(Imovel): Implementa o cálculo de base, adicional de 2 quartos, vaga de garagem e a regra polimórfica de 5% de desconto para locatários sem crianças.
* Casa(Imovel): Implementa o cálculo de base, adicional de 2 quartos e vaga de garagem.
* Estudio(Imovel): Implementa o cálculo de base e a regra específica do pacote de 2 vagas de estacionamento acrescido de vagas extras.
* ContratoLocacao: Utiliza composição com um objeto Imovel para gerenciar o parcelamento da taxa contratual (R$ 2.000,00 em até 5x), exibir o demonstrativo detalhado e exportar o arquivo CSV.
* SistemaRentSmart: Gerencia o fluxo de execução no terminal e realiza a validação rigorosa de todas as entradas do usuário.
________________


Pré-requisitos
* Python 3.10 ou superior instalado.
* Nenhuma biblioteca externa é necessária (utiliza apenas módulos nativos: abc, csv e os).
________________


Como Executar o Projeto
1. Clone este repositório ou baixe os arquivos para o seu computador:
git clone <URL_DO_SEU_REPOSITORIO_GITHUB>
cd <PASTA_DO_PROJETO>
2. Execute o arquivo principal pelo terminal:
python rentsmart.py
(Em sistemas Linux/macOS, utilize python3 rentsmart.py caso necessário.)
3. Siga as instruções exibidas no terminal informando:
   * Categoria do imóvel (1 - Apartamento, 2 - Casa ou 3 - Estúdio);
   * Quantidade de quartos ou configuração de estacionamento conforme a categoria;
   * Presença de crianças (para apartamentos);
   * Número de parcelas da taxa contratual (1 a 5).
4. Ao final, consulte o demonstrativo detalhado exibido na tela e abra o arquivo projecao_locacao_12_meses.csv gerado no diretório de execução.
________________


Exemplo de Saída Gerada
==================================================================
R.M IMÓVEIS — ORÇAMENTO DETALHADO DE LOCAÇÃO (RENTSMART)
==================================================================


[1] COMPOSIÇÃO DO ALUGUEL MENSAL RECORRENTE
------------------------------------------------------------------
  Aluguel-base (Apartamento - 1 quarto)                  R$ 700,00
  Adicional de quartos (2 quartos)                       R$ 200,00
  Vaga de garagem (Sim)                                  R$ 300,00
  Desconto comercial (5% - sem crianças)                 -R$ 60,00
------------------------------------------------------------------
  VALOR FINAL DO ALUGUEL MENSAL:                       R$ 1.140,00


[2] TAXA CONTRATUAL (CUSTO ADMINISTRATIVO SEPARADO)
------------------------------------------------------------------
  Valor total da taxa de contrato:                     R$ 2.000,00
  Condição de parcelamento escolhida:                  4x sem juros
  Valor da parcela (meses 1 a 4):                        R$ 500,00
  Observação: A taxa contratual não integra o aluguel mensal; após a 4ª parcela,
  o cliente pagará apenas o aluguel mensal.


[3] RESUMO FINANCEIRO DO PRIMEIRO ANO (12 MESES)
------------------------------------------------------------------
  Total previsto nos 12 meses (Aluguéis + Taxa):      R$ 15.680,00
==================================================================
