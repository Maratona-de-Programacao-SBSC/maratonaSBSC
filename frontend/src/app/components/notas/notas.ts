import { Component, Input } from '@angular/core';

import { ApiService } from '../../services/api';

@Component({
  selector: 'app-notas',
  standalone: true,
  imports: [],
  templateUrl: './notas.html',
  styleUrl: './notas.scss'
})
export class NotasComponent {

  private _cnpj = '';

  @Input() set cnpj(value: string) {
    if (!value) return;
    this._cnpj = value;
    this.carregarNotas();
  }

  notas: any[] = [];
  modalAberto = false;
  itens: any[] = [];
  notaSelecionada: any = null;

  constructor(private api: ApiService) {}

  carregarNotas() {
    this.api.buscarNotas(this._cnpj)
      .subscribe((res: any) => {
        this.notas = res;
      });
  }

  abrirNota(registro: any) {
    this.notaSelecionada = registro.nota;
    this.itens = registro.itens;
    this.modalAberto = true;
  }

  fechar() {
    this.modalAberto = false;
    this.itens = [];
    this.notaSelecionada = null;
  }
}