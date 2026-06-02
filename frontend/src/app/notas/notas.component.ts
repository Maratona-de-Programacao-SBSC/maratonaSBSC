import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../shared/api.service';

@Component({
  selector: 'app-notas',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="page">
      <div class="page-header">
        <h1>Notas Fiscais</h1>
        <p>Busque e importe notas fiscais por CNPJ</p>
      </div>

      <!-- Importar novas notas -->
      <div class="card">
        <h2>Importar Notas</h2>
        <div class="form-row">
          <input [(ngModel)]="cnpjInput" placeholder="CNPJ (só números)" class="input" maxlength="14" />
          <button (click)="importar()" [disabled]="loading" class="btn-primary">
            {{ loading ? 'Buscando...' : 'Buscar e Salvar' }}
          </button>
        </div>
        <div *ngIf="resultado" class="resultado">
          <span class="badge valid">✓ {{ resultado.salvas }} válidas</span>
          <span class="badge suspect" *ngIf="resultado.suspeitas > 0">⚠ {{ resultado.suspeitas }} suspeitas</span>
          <span class="badge invalid" *ngIf="resultado.invalidas > 0">✗ {{ resultado.invalidas }} inválidas</span>
        </div>
      </div>

      <!-- Filtros -->
      <div class="filters">
        <button (click)="filtrar(null)" [class.active]="filtroStatus === null" class="filter-btn">Todas</button>
        <button (click)="filtrar('valida')" [class.active]="filtroStatus === 'valida'" class="filter-btn valid">Válidas</button>
        <button (click)="filtrar('suspeita')" [class.active]="filtroStatus === 'suspeita'" class="filter-btn suspect">Suspeitas</button>
      </div>

      <!-- Tabela -->
      <div class="table-wrapper">
        <table *ngIf="notas.length > 0; else empty">
          <thead>
            <tr>
              <th>Fornecedor</th>
              <th>CNPJ</th>
              <th>Órgão Destinatário</th>
              <th>Valor</th>
              <th>Emissão</th>
              <th>Status</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let nota of notas" [class.row-suspect]="nota.status === 'suspeita'">
              <td>{{ nota.razao_social_emitente }}</td>
              <td class="mono">{{ nota.cpf_cnpj_emitente }}</td>
              <td>{{ nota.orgao_destinatario }}</td>
              <td class="valor">R$ {{ nota.valor | number:'1.2-2' }}</td>
              <td>{{ nota.data_emissao }}</td>
              <td>
                <span class="badge" [ngClass]="nota.status">{{ nota.status }}</span>
              </td>
              <td>
                <button class="btn-link" (click)="verItens(nota)">Ver itens</button>
              </td>
            </tr>
          </tbody>
        </table>
        <ng-template #empty>
          <p class="empty">Nenhuma nota encontrada.</p>
        </ng-template>
      </div>

      <!-- Modal de itens -->
      <div class="modal-overlay" *ngIf="notaSelecionada" (click)="fecharModal()">
        <div class="modal" (click)="$event.stopPropagation()">
          <div class="modal-header">
            <h3>Itens da Nota</h3>
            <button (click)="fecharModal()" class="btn-close">✕</button>
          </div>
          <p class="modal-sub">{{ notaSelecionada.razao_social_emitente }}</p>
          <table *ngIf="itens.length > 0">
            <thead>
              <tr>
                <th>#</th>
                <th>Descrição</th>
                <th>NCM</th>
                <th>Qtd</th>
                <th>Unidade</th>
                <th>Vlr Unit.</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              <tr *ngFor="let item of itens">
                <td>{{ item.numero_produto }}</td>
                <td>{{ item.descricao }}</td>
                <td class="mono">{{ item.codigo_ncm }}</td>
                <td>{{ item.quantidade }}</td>
                <td>{{ item.unidade }}</td>
                <td>R$ {{ item.valor_unitario | number:'1.2-2' }}</td>
                <td class="valor">R$ {{ item.valor | number:'1.2-2' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `,
})
export class NotasComponent {
  cnpjInput = '';
  loading = false;
  resultado: any = null;
  notas: any[] = [];
  filtroStatus: string | null = null;
  notaSelecionada: any = null;
  itens: any[] = [];

  constructor(private api: ApiService) {
    this.filtrar(null);
  }

  importar() {
    if (!this.cnpjInput) return;
    this.loading = true;
    this.resultado = null;
    this.api.buscarNotas(this.cnpjInput).subscribe({
      next: (res) => {
        this.resultado = res;
        this.loading = false;
        this.filtrar(this.filtroStatus);
      },
      error: () => { this.loading = false; }
    });
  }

  filtrar(status: string | null) {
    this.filtroStatus = status;
    this.api.listarNotas(status ?? undefined).subscribe(d => this.notas = d);
  }

  verItens(nota: any) {
    this.notaSelecionada = nota;
    this.api.listarItensDaNota(nota.chave_acesso).subscribe(d => this.itens = d);
  }

  fecharModal() {
    this.notaSelecionada = null;
    this.itens = [];
  }
}