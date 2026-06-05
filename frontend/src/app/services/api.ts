import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private http = inject(HttpClient);

  private readonly api = 'http://localhost:8000';

  buscarInformacoes(cnpj: string) {
    return this.http.get(
      `${this.api}/cnpj/informacoes/${cnpj}`
    );
  }

  buscarDespesas(cnpj: string) {
    return this.http.get(
      `${this.api}/cnpj/despesas/${cnpj}`
    );
  }

  buscarNotas(cnpj: string) {
    return this.http.get(
      `${this.api}/cnpj/notas/${cnpj}`
    );
  }

}