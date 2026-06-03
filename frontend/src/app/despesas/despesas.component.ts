import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../shared/api.service';

@Component({
  selector: 'app-despesas',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="page">
      <div class="page-header">
        <h1>Despesas Públicas</h1>
        <p>Importe e visualize empenhos, liquidações e pagamentos</p>
      </div>

      <!-- Importar -->
      <div class="card">
        <h2>Importar Despesas</h2>
        <div class="form-row">
          <div class="field">
            <label>Data Início</label>
            <input [(ngModel)]="dataInicio" placeholder="YYYYMMDD" class="input" />
          </div>
          <div class="field">
            <label>Data Fim</label>
            <input [(ngModel)]="dataFim" placeholder="YYYYMMDD" class="input" />
          </div>
          <button (click)="importar()" [disabled]="importando" class="btn-primary">
            {{ importando ? 'Iniciando...' : 'Importar' }}
          </button>
        </div>
        <div *ngIf="msgImport" class="resultado">
          <span class="badge valid">{{ msgImport }}</span>
        </div>
      </div>

      <!-- Tabs -->
      <div class="tabs">
        <button (click)="aba = 'empenhos'" [class.active]="aba === 'empenhos'" class="tab">Empenhos</button>
        <button (click)="aba = 'pagamentos'" [class.active]="aba === 'pagamentos'" class="tab">Pagamentos</button>
        <button (click)="aba = 'liquidacoes'" [class.active]="aba === 'liquidacoes'" class="tab">Liquidações</button>
      </div>

      <!-- Empenhos -->
      <div class="table-wrapper" *ngIf="aba === 'empenhos'">
        <table *ngIf="empenhos.length > 0; else empty">
          <thead>
            <tr>
              <th>Código</th>
              <th>Favorecido</th>
              <th>Tipo</th>
              <th>Elemento</th>
              <th>Emissão</th>
              <th>Valor</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let e of empenhos">
              <td class="mono">{{ e.codigo_empenho }}</td>
              <td>{{ e.favorecido }}</td>
              <td>{{ e.tipo_empenho }}</td>
              <td>{{ e.elemento_despesa }}</td>
              <td>{{ e.data_emissao }}</td>
              <td class="valor">R$ {{ e.valor | number:'1.2-2' }}</td>
            </tr>
          </tbody>
        </table>
        <ng-template #empty><p class="empty">Nenhum empenho encontrado.</p></ng-template>
      </div>

      <!-- Pagamentos -->
      <div class="table-wrapper" *ngIf="aba === 'pagamentos'">
        <table *ngIf="pagamentos.length > 0; else empty2">
          <thead>
            <tr>
              <th>Código</th>
              <th>Favorecido</th>
              <th>Órgão</th>
              <th>Processo</th>
              <th>Emissão</th>
              <th>Valor</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let p of pagamentos">
              <td class="mono">{{ p.codigo_pagamento }}</td>
              <td>{{ p.favorecido }}</td>
              <td>{{ p.orgao }}</td>
              <td class="mono">{{ p.processo }}</td>
              <td>{{ p.data_emissao }}</td>
              <td class="valor">R$ {{ p.valor | number:'1.2-2' }}</td>
            </tr>
          </tbody>
        </table>
        <ng-template #empty2><p class="empty">Nenhum pagamento encontrado.</p></ng-template>
      </div>

      <!-- Liquidações -->
      <div class="table-wrapper" *ngIf="aba === 'liquidacoes'">
        <table *ngIf="liquidacoes.length > 0; else empty3">
          <thead>
            <tr>
              <th>Código</th>
              <th>Favorecido</th>
              <th>Elemento</th>
              <th>Emissão</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let l of liquidacoes">
              <td class="mono">{{ l.codigo_liquidacao }}</td>
              <td>{{ l.favorecido }}</td>
              <td>{{ l.codigo_elemento_despesa }}</td>
              <td>{{ l.data_emissao }}</td>
            </tr>
          </tbody>
        </table>
        <ng-template #empty3><p class="empty">Nenhuma liquidação encontrada.</p></ng-template>
      </div>
    </div>
  `,
})
export class DespesasComponent implements OnInit {
  dataInicio = '';
  dataFim = '';
  importando = false;
  msgImport = '';
  aba = 'empenhos';
  empenhos: any[] = [];
  pagamentos: any[] = [];
  liquidacoes: any[] = [];

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.api.listarEmpenhos().subscribe(d => this.empenhos = d);
    this.api.listarPagamentos().subscribe(d => this.pagamentos = d);
    this.api.listarLiquidacoes().subscribe(d => this.liquidacoes = d);
  }

  importar() {
    if (!this.dataInicio || !this.dataFim) return;
    this.importando = true;
    this.api.importarDespesas(this.dataInicio, this.dataFim).subscribe({
      next: (res) => {
        this.msgImport = res.status + ' — processando em background';
        this.importando = false;
      },
      error: () => { this.importando = false; }
    });
  }
}