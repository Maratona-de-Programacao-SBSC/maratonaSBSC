import { of } from 'rxjs';

export const apiServiceMock = {
  buscarInformacoes: () =>
    of({ codigo_favorecido: '12345678000199', razao_social: 'Empresa teste' }),
  buscarInfosExternas: () => of({ cnpj: '12345678000199', razao_social: 'Empresa teste' }),
  buscarResumoDespesas: () =>
    of({
      empenhos: { total: 0, soma: 0 },
      liquidacoes: { total: 0, soma: 0 },
      pagamentos: { total: 0, soma: 0 },
    }),
  buscarEmpenhos: () => of([]),
  buscarLiquidacoes: () => of([]),
  buscarPagamentos: () => of([]),
  buscarNotas: () => of({ notas: [], total: 0, pagina: 0, tamanho: 10, total_paginas: 0 }),
  buscarItensNota: () => of([]),
  buscarAvaliacao: () => of({ cnpj: '12345678000199', votos_cidadaos: 0 }),
  votar: () => of({ cnpj: '12345678000199', votos_cidadaos: 1 }),
  buscarRanking: () => of([]),
  mensagemErro: (_error: unknown, fallback = 'Erro') => fallback,
  temInfosExternas: () => false,
  getNomeCache: () => null,
};
