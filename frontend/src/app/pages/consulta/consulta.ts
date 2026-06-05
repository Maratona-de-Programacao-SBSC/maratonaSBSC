import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { ApiService } from '../../services/api';

import { DespesasComponent } from '../../components/despesas/despesas';
import { NotasComponent } from '../../components/notas/notas';

@Component({
  selector: 'app-consultas',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    DespesasComponent,
    NotasComponent
  ],
  templateUrl: './consulta.html',
  styleUrls: ['./consulta.scss']
})
export class ConsultasComponent {

  cnpj = '';

  resultado: any = null;

  aba: 'despesas' | 'notas' | 'outros' = 'despesas';

  constructor(
    private api: ApiService
  ) {}
  loading = false;
  pesquisar() {

    const cnpj = this.cnpj.trim();

    if (!cnpj) {
      return;
    }

    this.loading = true;

    this.api.buscarDespesas(cnpj)
      .subscribe({
        next: (res) => {

          console.log('SUCESSO', res);

          this.resultado = res;
          this.loading = false;

        },
        error: (err) => {

          console.error('ERRO', err);

          this.loading = false;
        },
        complete: () => {
          console.log('COMPLETE');
        }
      });
    }
}