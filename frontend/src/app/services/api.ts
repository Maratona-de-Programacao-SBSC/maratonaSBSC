import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private http = inject(HttpClient);
  private readonly api = 'http://localhost:8000';

  private cacheDespesas  = new Map<string, any>();
  private cacheNotas     = new Map<string, any>();
  private cacheEmpresas  = new Map<string, any>();

  buscarInformacoes(cnpj: string): Observable<any> {
    if (this.cacheEmpresas.has(cnpj)) {
      return of(this.cacheEmpresas.get(cnpj));
    }
    return this.http.get(`${this.api}/cnpj/informacoes/${cnpj}`).pipe(
      tap(res => this.cacheEmpresas.set(cnpj, res))
    );
  }

  buscarDespesas(cnpj: string): Observable<any> {
    if (this.cacheDespesas.has(cnpj)) {
      return of(this.cacheDespesas.get(cnpj));
    }
    return this.http.get(`${this.api}/cnpj/despesas/${cnpj}`).pipe(
      tap(res => this.cacheDespesas.set(cnpj, res))
    );
  }

  buscarNotas(cnpj: string, pagina: number = 0): Observable<any> {
    const key = `${cnpj}_p${pagina}`;
    if (this.cacheNotas.has(key)) {
      return of(this.cacheNotas.get(key));
    }
    return this.http.get(`${this.api}/cnpj/notas/${cnpj}?pagina=${pagina}&tamanho=10`).pipe(
      tap(res => this.cacheNotas.set(key, res))
    );
  }

  buscarItensNota(cnpj: string, chave: string): Observable<any> {
    const key = `itens_${chave}`;
    if (this.cacheNotas.has(key)) {
      return of(this.cacheNotas.get(key));
    }
    return this.http.get(`${this.api}/cnpj/notas/${cnpj}/itens/${chave}`).pipe(
      tap(res => this.cacheNotas.set(key, res))
    );
  }

  buscarInfosExternas(cnpj: string): Observable<any> {
    const salvo = localStorage.getItem(`brasilapi_${cnpj}`);
    if (salvo) {
      return of(JSON.parse(salvo));
    }
    return this.http.get(`https://brasilapi.com.br/api/cnpj/v1/${cnpj}`).pipe(
      tap(res => localStorage.setItem(`brasilapi_${cnpj}`, JSON.stringify(res)))
    );
  }

  temInfosExternas(cnpj: string): boolean {
    return localStorage.getItem(`brasilapi_${cnpj}`) !== null;
  }

  getNomeCache(cnpj: string): string | null {
    const salvo = localStorage.getItem(`brasilapi_${cnpj}`);
    if (!salvo) return null;
    return JSON.parse(salvo)?.razao_social ?? null;
  }

  buscarAvaliacao(cnpj: string): Observable<any> {
    return this.http.get(`${this.api}/avaliacao/${cnpj}`);
  }

  votar(cnpj: string): Observable<any> {
    return this.http.post(`${this.api}/avaliacao/${cnpj}/votar`, {});
  }

  buscarRanking(): Observable<any> {
      return this.http.get(`${this.api}/avaliacao/ranking?limit=5`);
    }
  buscarResumoDespesas(cnpj: string): Observable<any> {
    const key = `resumo_${cnpj}`;
    if (this.cacheDespesas.has(key)) {
      return of(this.cacheDespesas.get(key));
    }
    return this.http.get(`${this.api}/cnpj/despesas/${cnpj}/resumo`).pipe(
      tap(res => this.cacheDespesas.set(key, res))
    );
  }

  buscarEmpenhos(cnpj: string, pagina: number = 0): Observable<any> {
    const key = `emp_${cnpj}_p${pagina}`;
    if (this.cacheDespesas.has(key)) {
      return of(this.cacheDespesas.get(key));
    }
    return this.http.get(`${this.api}/cnpj/despesas/${cnpj}/empenhos?pagina=${pagina}&tamanho=10`).pipe(
      tap(res => this.cacheDespesas.set(key, res))
    );
  }

  buscarLiquidacoes(cnpj: string, pagina: number = 0): Observable<any> {
    const key = `liq_${cnpj}_p${pagina}`;
    if (this.cacheDespesas.has(key)) {
      return of(this.cacheDespesas.get(key));
    }
    return this.http.get(`${this.api}/cnpj/despesas/${cnpj}/liquidacoes?pagina=${pagina}&tamanho=10`).pipe(
      tap(res => this.cacheDespesas.set(key, res))
    );
  }

  buscarPagamentos(cnpj: string, pagina: number = 0): Observable<any> {
    const key = `pag_${cnpj}_p${pagina}`;
    if (this.cacheDespesas.has(key)) {
      return of(this.cacheDespesas.get(key));
    }
    return this.http.get(`${this.api}/cnpj/despesas/${cnpj}/pagamentos?pagina=${pagina}&tamanho=10`).pipe(
      tap(res => this.cacheDespesas.set(key, res))
    );
  }
  limparCache() {
    this.cacheDespesas.clear();
    this.cacheNotas.clear();
    this.cacheEmpresas.clear();
  }
}