import { Component, Input, OnChanges, SimpleChanges, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-despesas',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './despesas.html',
  styleUrls: ['./despesas.scss']
})
export class DespesasComponent implements OnChanges {

  @Input() cnpj = '';

  resumo: any = null;
  empenhos: any[] = [];
  liquidacoes: any[] = [];
  pagamentos: any[] = [];

  paginaEmpenhos = 0;
  paginaLiquidacoes = 0;
  paginaPagamentos = 0;

  readonly tamanho = 10;

  modalAberto = false;
  itemSelecionado: any = null;
  tipoModal: 'empenho' | 'liquidacao' | 'pagamento' | null = null;

  constructor(
    private api: ApiService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnChanges(changes: SimpleChanges) {
    if (changes['cnpj'] && this.cnpj) {
      this.paginaEmpenhos = 0;
      this.paginaLiquidacoes = 0;
      this.paginaPagamentos = 0;
      this.carregar();
    }
  }

  carregar() {
    this.api.buscarResumoDespesas(this.cnpj).subscribe((res: any) => {
      this.resumo = res;
      this.cdr.detectChanges();
    });

    this.carregarEmpenhos();
    this.carregarLiquidacoes();
    this.carregarPagamentos();
  }

  carregarEmpenhos() {
    this.api.buscarEmpenhos(this.cnpj, this.paginaEmpenhos).subscribe((res: any) => {
      this.empenhos = res;
      this.cdr.detectChanges();
    });
  }

  carregarLiquidacoes() {
    this.api.buscarLiquidacoes(this.cnpj, this.paginaLiquidacoes).subscribe((res: any) => {
      this.liquidacoes = res;
      this.cdr.detectChanges();
    });
  }

  carregarPagamentos() {
    this.api.buscarPagamentos(this.cnpj, this.paginaPagamentos).subscribe((res: any) => {
      this.pagamentos = res;
      this.cdr.detectChanges();
    });
  }

  mudarPaginaEmpenhos(p: number) { this.paginaEmpenhos = p; this.carregarEmpenhos(); }
  mudarPaginaLiquidacoes(p: number) { this.paginaLiquidacoes = p; this.carregarLiquidacoes(); }
  mudarPaginaPagamentos(p: number) { this.paginaPagamentos = p; this.carregarPagamentos(); }

  get totalEmpenhado(): number {
    return Number(this.resumo?.empenhos?.soma || 0);
  }

  get totalLiquidado(): number {
    return Number(this.resumo?.liquidacoes?.soma || 0);
  }

  get totalPago(): number {
    return Number(this.resumo?.pagamentos?.soma || 0);
  }

  get totalPaginasEmpenhos(): number {
    return Math.ceil((this.resumo?.empenhos?.total || 0) / this.tamanho);
  }

  get totalPaginasLiquidacoes(): number {
    return Math.ceil((this.resumo?.liquidacoes?.total || 0) / this.tamanho);
  }

  get totalPaginasPagamentos(): number {
    return Math.ceil((this.resumo?.pagamentos?.total || 0) / this.tamanho);
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