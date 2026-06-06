import { Component, ViewChild, ElementRef } from '@angular/core';
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
  loading = false;
  aba: 'despesas' | 'notas' | 'outros' = 'despesas';

  constructor(private api: ApiService) {}

  pesquisar() {
    this.cnpj = this.inputCnpj.nativeElement.value.trim();
    if (!this.cnpj) return;

    this.loading = true;
    this.aba = 'despesas';

    this.api.buscarDespesas(this.cnpj).subscribe({
      next: (res) => {
        this.resultado = res;
        this.loading = false;
      },
      error: (err) => {
        console.error('ERRO', err);
        this.loading = false;
      }
    });
  }
}