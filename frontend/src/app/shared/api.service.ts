import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private base = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  // Notas
  buscarNotas(cnpj: string, pagina = 1): Observable<any> {
    const params = new HttpParams().set('cnpj', cnpj).set('pagina', pagina);
    return this.http.get(`${this.base}/notas`, { params });
  }

  // DB - Notas salvas
  listarNotas(status?: string, limite = 100, pagina = 1): Observable<any[]> {
    let params = new HttpParams().set('limite', limite).set('pagina', pagina);
    if (status) params = params.set('status', status);
    return this.http.get<any[]>(`${this.base}/db/notas`, { params });
  }

  listarItensDaNota(chaveAcesso: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.base}/db/notas/${chaveAcesso}/itens`);
  }

  // DB - Despesas
  listarEmpenhos(limite = 100, pagina = 1): Observable<any[]> {
    const params = new HttpParams().set('limite', limite).set('pagina', pagina);
    return this.http.get<any[]>(`${this.base}/db/empenhos`, { params });
  }

  listarPagamentos(limite = 100, pagina = 1): Observable<any[]> {
    const params = new HttpParams().set('limite', limite).set('pagina', pagina);
    return this.http.get<any[]>(`${this.base}/db/pagamentos`, { params });
  }

  listarLiquidacoes(limite = 100, pagina = 1): Observable<any[]> {
    const params = new HttpParams().set('limite', limite).set('pagina', pagina);
    return this.http.get<any[]>(`${this.base}/db/liquidacoes`, { params });
  }

  // Importar despesas
  importarDespesas(dataInicio: string, dataFim: string): Observable<any> {
    const params = new HttpParams()
      .set('data_inicio', dataInicio)
      .set('data_fim', dataFim);
    return this.http.post(`${this.base}/despesas/importar`, {}, { params });
  }

  // Contratos
  listarContratos(dataInicial: string, dataFinal: string, pagina = 1): Observable<any> {
    const params = new HttpParams()
      .set('data_inicial', dataInicial)
      .set('data_final', dataFinal)
      .set('pagina', pagina);
    return this.http.get(`${this.base}/contratos`, { params });
  }
}