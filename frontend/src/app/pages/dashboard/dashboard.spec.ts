import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss'
})
export class DashboardComponent {
  cnpj = '';

  empresa: any = null;

  empenhos: any[] = [];
  liquidacoes: any[] = [];
  pagamentos: any[] = [];

  resumo: any = null;

  constructor(private http: HttpClient) {}

  pesquisar() {
    this.http
      .get<any>(`http://localhost:8000/dados/cnpj/${this.cnpj}`)
      .subscribe(res => {
        this.empresa = res.empresa;

        this.empenhos = res.empenhos || [];
        this.liquidacoes = res.liquidacoes || [];
        this.pagamentos = res.pagamentos || [];

        this.resumo = res.resumo;
      });
  }
}