import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../shared/api.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="dashboard">
      <div class="stats-grid">
        <div class="stat-card valid">
          <span class="stat-label">Notas Válidas</span>
          <span class="stat-value">{{ counts.validas }}</span>
        </div>
        <div class="stat-card suspect">
          <span class="stat-label">Suspeitas</span>
          <span class="stat-value">{{ counts.suspeitas }}</span>
        </div>
        <div class="stat-card neutral">
          <span class="stat-label">Empenhos</span>
          <span class="stat-value">{{ counts.empenhos }}</span>
        </div>
        <div class="stat-card neutral">
          <span class="stat-label">Pagamentos</span>
          <span class="stat-value">{{ counts.pagamentos }}</span>
        </div>
      </div>

      <div class="recent-section">
        <h2>Notas Recentes Suspeitas</h2>
        <table *ngIf="notasSuspeitas.length > 0; else empty">
          <thead>
            <tr>
              <th>Fornecedor</th>
              <th>CNPJ</th>
              <th>Valor</th>
              <th>Emissão</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let nota of notasSuspeitas">
              <td>{{ nota.razao_social_emitente }}</td>
              <td class="mono">{{ nota.cpf_cnpj_emitente }}</td>
              <td class="valor">R$ {{ nota.valor | number:'1.2-2' }}</td>
              <td>{{ nota.data_emissao }}</td>
              <td><span class="badge suspect">suspeita</span></td>
            </tr>
          </tbody>
        </table>
        <ng-template #empty>
          <p class="empty">Nenhuma nota suspeita encontrada.</p>
        </ng-template>
      </div>
    </div>
  `,
})
export class DashboardComponent implements OnInit {
  counts = { validas: 0, suspeitas: 0, empenhos: 0, pagamentos: 0 };
  notasSuspeitas: any[] = [];

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.api.listarNotas('valida', 1).subscribe(d => this.counts.validas = d.length);
    this.api.listarNotas('suspeita', 100).subscribe(d => {
      this.counts.suspeitas = d.length;
      this.notasSuspeitas = d.slice(0, 10);
    });
    this.api.listarEmpenhos(1).subscribe(d => this.counts.empenhos = d.length);
    this.api.listarPagamentos(1).subscribe(d => this.counts.pagamentos = d.length);
  }
}