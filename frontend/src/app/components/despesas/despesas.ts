import { Component, Input, OnChanges, SimpleChanges, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-despesas',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './despesas.html',
  styleUrls: ['./despesas.scss']
})
export class DespesasComponent implements OnChanges {

  @Input() resultado: any;

  modalAberto = false;
  itemSelecionado: any = null;
  tipoModal: 'empenho' | 'liquidacao' | 'pagamento' | null = null;

  readonly pageSize = 10;

  paginaEmpenhos = 0;
  paginaLiquidacoes = 0;
  paginaPagamentos = 0;

  constructor(private cdr: ChangeDetectorRef) {}

  ngOnChanges(changes: SimpleChanges) {
    if (changes['resultado']) {
      this.paginaEmpenhos = 0;
      this.paginaLiquidacoes = 0;
      this.paginaPagamentos = 0;
      this.cdr.detectChanges();
    }
  }

  get totalEmpenhado(): number {
    return (this.resultado?.empenhos || [])
      .reduce((soma: number, item: any) => soma + Number(item.valor || 0), 0);
  }

  get totalLiquidado(): number {
    return (this.resultado?.liquidacoes || [])
      .reduce((soma: number, item: any) => soma + Number(item.valor || 0), 0);
  }

  get totalPago(): number {
    return (this.resultado?.pagamentos || [])
      .reduce((soma: number, item: any) => soma + Number(item.valor || 0), 0);
  }

  paginar(lista: any[], pagina: number): any[] {
    const inicio = pagina * this.pageSize;
    return (lista || []).slice(inicio, inicio + this.pageSize);
  }

  totalPaginas(lista: any[]): number {
    return Math.ceil((lista || []).length / this.pageSize);
  }

  abrirModal(item: any, tipo: 'empenho' | 'liquidacao' | 'pagamento') {
    this.itemSelecionado = item;
    this.tipoModal = tipo;
    this.modalAberto = true;
    this.cdr.detectChanges();
  }

  fechar() {
    this.modalAberto = false;
    this.itemSelecionado = null;
    this.tipoModal = null;
    this.cdr.detectChanges();
  }
}