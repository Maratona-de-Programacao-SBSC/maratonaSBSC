import { Component, Input, ChangeDetectorRef, OnChanges, SimpleChanges } from '@angular/core';
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-notas',
  standalone: true,
  imports: [],
  templateUrl: './notas.html',
  styleUrl: './notas.scss'
})
export class NotasComponent implements OnChanges {

  private _cnpj = '';

  @Input() cnpj = '';

  notas: any[] = [];
  modalAberto = false;
  itens: any[] = [];
  notaSelecionada: any = null;

  constructor(
    private api: ApiService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnChanges(changes: SimpleChanges) {
    if (changes['cnpj']) {
      const novo = changes['cnpj'].currentValue;

      if (novo && novo !== this._cnpj) {
        this._cnpj = novo;
        this.notas = [];
        this.fechar();
        this.carregarNotas();
      }
      // se vier '' (saiu da aba) — não faz nada, mantém os dados
    }
  }

  carregarNotas() {
    this.api.buscarNotas(this._cnpj)
      .subscribe((res: any) => {
        this.notas = res;
        this.cdr.detectChanges();
      });
  }

  abrirNota(registro: any) {
    this.notaSelecionada = registro.nota;
    this.itens = registro.itens;
    this.modalAberto = true;
    this.cdr.detectChanges();
  }

  fechar() {
    this.modalAberto = false;
    this.itens = [];
    this.notaSelecionada = null;
    this.cdr.detectChanges();
  }
}