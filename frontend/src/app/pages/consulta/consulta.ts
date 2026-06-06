import { Component, ViewChild, ElementRef, NgZone, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { ApiService } from '../../services/api';
import { DespesasComponent } from '../../components/despesas/despesas';
import { NotasComponent } from '../../components/notas/notas';

@Component({
  selector: 'app-consultas',
  standalone: true,
  imports: [CommonModule, FormsModule, DespesasComponent, NotasComponent],
  templateUrl: './consulta.html',
  styleUrls: ['./consulta.scss']
})
export class ConsultasComponent {

  @ViewChild('inputCnpj') inputCnpj!: ElementRef;

  cnpj = '';
  resultado: any = null;
  empresa: any = null; 
  loadingDespesas = false;
  aba: 'despesas' | 'notas' | 'outros' = 'despesas';

  constructor(
    private api: ApiService,
    private zone: NgZone,
    private cdr: ChangeDetectorRef
  ) {}

  pesquisar() {
    this.cnpj = this.inputCnpj.nativeElement.value.trim();
    if (!this.cnpj) return;

    this.aba = 'despesas';
    this.resultado = null;
    this.empresa = null;
    this.loadingDespesas = true;
    this.cdr.detectChanges();

    this.api.buscarDespesas(this.cnpj).subscribe({
      next: (res) => {
        this.zone.run(() => {
          this.resultado = res;
          this.loadingDespesas = false;
          this.cdr.detectChanges();
        });
      },
      error: (err) => {
        this.zone.run(() => {
          console.error('ERRO', err);
          this.loadingDespesas = false;
          this.cdr.detectChanges();
        });
      }
    });

    this.api.buscarInformacoes(this.cnpj).subscribe({
      next: (res) => {
        this.zone.run(() => {
          this.empresa = res;
          this.cdr.detectChanges();
        });
      }
    });
  }
}