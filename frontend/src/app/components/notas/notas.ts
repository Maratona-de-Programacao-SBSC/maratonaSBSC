import { Component, Input, ChangeDetectorRef, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-notas',
  standalone: true,
  imports: [CommonModule],
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
  loadingItens = false;

  pagina = 0;
  totalPaginas = 0;
  total = 0;

  constructor(
    private api: ApiService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnChanges(changes: SimpleChanges) {
    if (changes['cnpj']) {
      const novo = changes['cnpj'].currentValue;
      if (novo && novo !== this._cnpj) {
        this._cnpj = novo;
        this.pagina = 0;
        this.notas = [];
        this.fechar();
        this.carregarNotas();
      }
    }
  }

  carregarNotas() {
    this.api.buscarNotas(this._cnpj, this.pagina).subscribe((res: any) => {
      this.notas = res.notas;
      this.total = res.total;
      this.totalPaginas = res.total_paginas;
      this.cdr.detectChanges();
    });
  }

  mudarPagina(pagina: number) {
    this.pagina = pagina;
    this.carregarNotas();
  }

  abrirNota(nota: any) {
    this.notaSelecionada = nota;
    this.itens = [];
    this.loadingItens = true;
    this.modalAberto = true;
    this.cdr.detectChanges();

    this.api.buscarItensNota(this._cnpj, nota.chave_acesso).subscribe((res: any) => {
      this.itens = res;
      this.loadingItens = false;
      this.cdr.detectChanges();
    });
  }

  fechar() {
    this.modalAberto = false;
    this.itens = [];
    this.notaSelecionada = null;
    this.loadingItens = false;
    this.cdr.detectChanges();
  }
}