import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private http = inject(HttpClient);

  private readonly api = 'http://localhost:8000';

  getEmpenhos(limit = 100) {
    return this.http.get(`${this.api}/dados/empenhos?limit=${limit}`);
  }

  getLiquidacoes(limit = 100) {
    return this.http.get(`${this.api}/dados/liquidacoes?limit=${limit}`);
  }

  getPagamentos(limit = 100) {
    return this.http.get(`${this.api}/dados/pagamentos?limit=${limit}`);
  }

  getEmpresas(limit = 100) {
    return this.http.get(`${this.api}/dados/informacoes-cnpj?limit=${limit}`);
  }

  buscarEmpresa(cnpj: string) {
    return this.http.get(`${this.api}/dados/informacoes-cnpj/${cnpj}`);
  }
  buscarEmpenhosPorCnpj(cnpj: string) {
  return this.http.get(
    `${this.api}/dados/empenhos/cnpj/${cnpj}`
  );
  }

  buscarLiquidacoesPorCnpj(cnpj: string) {
    return this.http.get(
      `${this.api}/dados/liquidacoes/cnpj/${cnpj}`
    );
  }

  buscarPagamentosPorCnpj(cnpj: string) {
    return this.http.get(
      `${this.api}/dados/pagamentos/cnpj/${cnpj}`
    );
  }
}