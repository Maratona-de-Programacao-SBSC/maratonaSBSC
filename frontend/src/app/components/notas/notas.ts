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

  readonly pageSize = 10;
  paginaNotas = 0;

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
        this.paginaNotas = 0;
        this.fechar();
        this.carregarNotas();
      }
    }
  }

  carregarNotas() {
    this.api.buscarNotas(this._cnpj).subscribe((res: any) => {
      this.notas = res;
      this.paginaNotas = 0;
      this.cdr.detectChanges();
    });
  }

  paginar(lista: any[], pagina: number): any[] {
    const inicio = pagina * this.pageSize;
    return (lista || []).slice(inicio, inicio + this.pageSize);
  }

  totalPaginas(): number {
    return Math.ceil(this.notas.length / this.pageSize);
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