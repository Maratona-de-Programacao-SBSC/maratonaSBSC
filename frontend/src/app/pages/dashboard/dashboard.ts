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
  resultado: any = null;

  constructor(private http: HttpClient) {}

  pesquisar() {
    this.http
      .get<any>(`http://localhost:8000/dados/cnpj/${this.cnpj}`)
      .subscribe(res => {
        console.log(res);
        this.resultado = res;
      });
  }

  notas: any[] = [];

carregarNotas() {
  this.http
    .get<any[]>('http://localhost:8000/dados/notas-fiscais?limit=50')
    .subscribe(res => {
      this.notas = res;
    });
}
}