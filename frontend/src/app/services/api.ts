import { HttpClient, HttpErrorResponse, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, catchError, of, shareReplay, throwError } from 'rxjs';
import {
  Avaliacao,
  CnpjSuspeito,
  Empenho,
  EmpresaBrasilApi,
  EmpresaLocal,
  ItemNotaFiscal,
  JobImportacao,
  JobImportacaoCriado,
  Liquidacao,
  NotaFiscal,
  Pagamento,
  PaginaNotas,
  ResumoDespesas,
  PeriodoImportacao,
  TipoImportacao,
} from '../models/api.models';

interface CacheEntry<T> {
  expiresAt: number;
  stream: Observable<T>;
}

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly http = inject(HttpClient);
  private readonly api = '/api';
  private readonly cache = new Map<string, CacheEntry<unknown>>();
  private readonly cacheTtlMs = 5 * 60 * 1000;

  buscarInformacoes(cnpj: string): Observable<EmpresaLocal> {
    return this.cached(`empresa:${cnpj}`, () =>
      this.http.get<EmpresaLocal>(`${this.api}/cnpj/informacoes/${cnpj}`),
    );
  }

  buscarInfosExternas(cnpj: string): Observable<EmpresaBrasilApi> {
    const key = `brasilapi_${cnpj}`;
    const salvo = this.lerLocalStorage<EmpresaBrasilApi>(key);
    if (salvo) return of(salvo);

    return this.cached(`externa:${cnpj}`, () =>
      this.http
        .get<EmpresaBrasilApi>(`https://brasilapi.com.br/api/cnpj/v1/${cnpj}`)
        .pipe(this.salvarRespostaLocal(key)),
    );
  }

  buscarResumoDespesas(cnpj: string): Observable<ResumoDespesas> {
    return this.cached(`resumo:${cnpj}`, () =>
      this.http.get<ResumoDespesas>(`${this.api}/cnpj/despesas/${cnpj}/resumo`),
    );
  }

  buscarEmpenhos(cnpj: string, pagina = 0): Observable<Empenho[]> {
    return this.buscarPagina<Empenho>(
      `empenhos:${cnpj}`,
      `${this.api}/cnpj/despesas/${cnpj}/empenhos`,
      pagina,
    );
  }

  buscarLiquidacoes(cnpj: string, pagina = 0): Observable<Liquidacao[]> {
    return this.buscarPagina<Liquidacao>(
      `liquidacoes:${cnpj}`,
      `${this.api}/cnpj/despesas/${cnpj}/liquidacoes`,
      pagina,
    );
  }

  buscarPagamentos(cnpj: string, pagina = 0): Observable<Pagamento[]> {
    return this.buscarPagina<Pagamento>(
      `pagamentos:${cnpj}`,
      `${this.api}/cnpj/despesas/${cnpj}/pagamentos`,
      pagina,
    );
  }

  buscarNotas(cnpj: string, pagina = 0): Observable<PaginaNotas> {
    const params = new HttpParams().set('pagina', pagina).set('tamanho', 10);
    return this.cached(`notas:${cnpj}:${pagina}`, () =>
      this.http.get<PaginaNotas>(`${this.api}/cnpj/notas/${cnpj}`, { params }),
    );
  }

  buscarItensNota(cnpj: string, chave: string): Observable<ItemNotaFiscal[]> {
    return this.cached(`itens:${cnpj}:${chave}`, () =>
      this.http.get<ItemNotaFiscal[]>(`${this.api}/cnpj/notas/${cnpj}/itens/${chave}`),
    );
  }

  buscarAvaliacao(cnpj: string): Observable<Avaliacao> {
    return this.http.get<Avaliacao>(`${this.api}/avaliacao/${cnpj}`);
  }

  votar(cnpj: string): Observable<Avaliacao> {
    return this.http.post<Avaliacao>(`${this.api}/avaliacao/${cnpj}/votar`, {});
  }

  buscarRanking(limite = 10): Observable<CnpjSuspeito[]> {
    const params = new HttpParams().set('limit', limite);
    return this.http.get<CnpjSuspeito[]>(`${this.api}/avaliacao/ranking`, { params });
  }

  iniciarImportacao(
    tipo: TipoImportacao,
    chaveAdministrativa: string,
    periodo?: PeriodoImportacao,
  ): Observable<JobImportacaoCriado> {
    const headers = this.cabecalhoAdministrativo(chaveAdministrativa);
    let params = new HttpParams();

    if (periodo) {
      params = params.set('data_inicio', periodo.dataInicio).set('data_fim', periodo.dataFim);
    }

    return this.http.post<JobImportacaoCriado>(
      `${this.api}/importacao/${tipo}`,
      {},
      { headers, params },
    );
  }

  consultarImportacao(jobId: string, chaveAdministrativa: string): Observable<JobImportacao> {
    return this.http.get<JobImportacao>(`${this.api}/importacao/jobs/${jobId}`, {
      headers: this.cabecalhoAdministrativo(chaveAdministrativa),
    });
  }

  temInfosExternas(cnpj: string): boolean {
    return this.lerLocalStorage<EmpresaBrasilApi>(`brasilapi_${cnpj}`) !== null;
  }

  getNomeCache(cnpj: string): string | null {
    return this.lerLocalStorage<EmpresaBrasilApi>(`brasilapi_${cnpj}`)?.razao_social ?? null;
  }

  limparCache(): void {
    this.cache.clear();
  }

  mensagemErro(error: unknown, fallback = 'Não foi possível concluir a solicitação.'): string {
    if (!(error instanceof HttpErrorResponse)) return fallback;
    if (error.status === 0)
      return 'Não foi possível conectar ao serviço. Tente novamente em instantes.';
    if (error.status === 401 || error.status === 403)
      return 'A chave administrativa informada não é válida.';
    if (error.status === 404) return 'Nenhum registro foi encontrado para este CNPJ.';
    if (error.status === 422) return 'Confira os dados informados e tente novamente.';
    if (error.status >= 500)
      return 'O serviço está temporariamente indisponível. Tente novamente mais tarde.';
    return fallback;
  }

  private cabecalhoAdministrativo(chaveAdministrativa: string): HttpHeaders {
    return new HttpHeaders().set('X-Admin-Key', chaveAdministrativa);
  }

  private buscarPagina<T>(key: string, url: string, pagina: number): Observable<T[]> {
    const params = new HttpParams().set('pagina', pagina).set('tamanho', 10);
    return this.cached(`${key}:${pagina}`, () => this.http.get<T[]>(url, { params }));
  }

  private cached<T>(key: string, request: () => Observable<T>): Observable<T> {
    const agora = Date.now();
    const entry = this.cache.get(key) as CacheEntry<T> | undefined;
    if (entry && entry.expiresAt > agora) return entry.stream;

    const stream = request().pipe(
      catchError((error) => {
        this.cache.delete(key);
        return throwError(() => error);
      }),
      shareReplay({ bufferSize: 1, refCount: false }),
    );
    this.cache.set(key, { expiresAt: agora + this.cacheTtlMs, stream });
    return stream;
  }

  private salvarRespostaLocal<T>(key: string) {
    return (source: Observable<T>) =>
      new Observable<T>((subscriber) =>
        source.subscribe({
          next: (value) => {
            try {
              localStorage.setItem(key, JSON.stringify(value));
            } catch {
              // O cache local é opcional e pode estar indisponível.
            }
            subscriber.next(value);
          },
          error: (error) => subscriber.error(error),
          complete: () => subscriber.complete(),
        }),
      );
  }

  private lerLocalStorage<T>(key: string): T | null {
    try {
      const value = localStorage.getItem(key);
      return value ? (JSON.parse(value) as T) : null;
    } catch {
      return null;
    }
  }
}
