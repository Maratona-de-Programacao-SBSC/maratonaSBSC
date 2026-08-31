export interface EmpresaLocal {
  codigo_favorecido: string;
  razao_social: string;
  nome_fantasia?: string | null;
  cod_cnae?: string | null;
  cod_natjuridica?: string | null;
  tipo_pessoa?: string | null;
  logradouro?: string | null;
  numero?: string | null;
  complemento?: string | null;
  cep?: string | null;
  bairro?: string | null;
  municipio?: string | null;
  uf?: string | null;
}

export interface Socio {
  cnpj_cpf_do_socio?: string;
  nome_socio: string;
  qualificacao_socio?: string;
}

export interface EmpresaBrasilApi {
  cnpj: string;
  razao_social: string;
  nome_fantasia?: string | null;
  descricao_situacao_cadastral?: string | null;
  opcao_pelo_simples?: boolean;
  opcao_pelo_mei?: boolean;
  natureza_juridica?: string | null;
  porte?: string | null;
  data_inicio_atividade?: string | null;
  cnae_fiscal_descricao?: string | null;
  descricao_tipo_de_logradouro?: string | null;
  logradouro?: string | null;
  numero?: string | null;
  complemento?: string | null;
  bairro?: string | null;
  municipio?: string | null;
  uf?: string | null;
  ddd_telefone_1?: string | null;
  email?: string | null;
  qsa?: Socio[];
}

export interface ResumoItem {
  total: number;
  soma: number | string;
}

export interface ResumoDespesas {
  empenhos: ResumoItem;
  liquidacoes: ResumoItem;
  pagamentos: ResumoItem;
}

export interface Empenho {
  id_empenho?: number;
  codigo_empenho: string;
  data_emissao: string;
  tipo_empenho?: string | null;
  codigo_orgao?: number | null;
  codigo_unidade_gestora?: number | null;
  codigo_favorecido: string;
  favorecido?: string | null;
  observacao?: string | null;
  elemento_despesa?: string | null;
  valor: number | string;
}

export interface Liquidacao {
  codigo_liquidacao: string;
  data_emissao: string;
  codigo_orgao?: number | null;
  codigo_unidade_gestora?: number | null;
  codigo_favorecido: string;
  favorecido?: string | null;
  observacao?: string | null;
  codigo_elemento_despesa?: string | null;
  valor: number | string;
}

export interface Pagamento {
  codigo_pagamento: string;
  data_emissao: string;
  codigo_favorecido: string;
  favorecido?: string | null;
  processo?: string | null;
  codigo_unidade_gestora?: number | null;
  codigo_orgao?: number | null;
  unidade_gestora?: string | null;
  orgao?: string | null;
  observacao?: string | null;
  valor: number | string;
}

export interface NotaFiscal {
  chave_acesso: string;
  data_emissao: string;
  codigo_favorecido: string;
  razao_social_emitente?: string | null;
  uf_emitente?: string | null;
  municipio_emitente?: string | null;
  orgao_destinatario?: string | null;
  cnpj_destinatario?: string | null;
  nome_destinatario?: string | null;
  uf_destinatario?: string | null;
  valor: number | string;
}

export interface ItemNotaFiscal {
  id?: number;
  numero_produto?: number;
  chave_nota: string;
  descricao?: string | null;
  codigo_ncm?: string | null;
  ncm?: string | null;
  cfop?: string | null;
  quantidade?: number | string | null;
  unidade?: string | null;
  valor_unitario?: number | string | null;
  valor?: number | string | null;
}

export interface PaginaNotas {
  notas: NotaFiscal[];
  total: number;
  pagina: number;
  tamanho: number;
  total_paginas: number;
}

export interface Avaliacao {
  cnpj: string;
  votos_cidadaos: number;
}

export interface CnpjSuspeito extends Avaliacao {
  razao_social?: string | null;
}
