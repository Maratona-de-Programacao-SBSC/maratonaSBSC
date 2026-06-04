from enum import Enum

class Documento(Enum):
    EMPENHOS = "Empenho"
    PAGAMENTOS = "Pagamento"
    LIQUIDACOES = "Liquidacao"
    NOTA_FISCAL = "NotaFiscal"
    ITEM_NOTA_FISCAL = "NotaFiscalItem"
    INFORMACOES_CNPJ = "Cnpj"