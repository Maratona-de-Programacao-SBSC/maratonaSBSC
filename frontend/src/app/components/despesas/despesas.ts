import {
  ChangeDetectionStrategy,
  Component,
  HostListener,
  Input,
  OnChanges,
  SimpleChanges,
  signal,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { finalize } from 'rxjs';
import { ApiService } from '../../services/api';
import { Empenho, Liquidacao, Pagamento, ResumoDespesas } from '../../models/api.models';
import { PaginationComponent } from '../ui/pagination/pagination';

type TipoDespesa = 'empenho' | 'liquidacao' | 'pagamento';
type RegistroDespesa = Empenho | Liquidacao | Pagamento;

@Component({
  selector: 'app-despesas',
  standalone: true,
  imports: [CommonModule, PaginationComponent],
  templateUrl: './despesas.html',
  styleUrls: ['./despesas.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DespesasComponent implements OnChanges {
  @Input() cnpj = '';

  readonly resumo = signal<ResumoDespesas | null>(null);
  readonly empenhos = signal<Empenho[]>([]);
  readonly liquidacoes = signal<Liquidacao[]>([]);
  readonly pagamentos = signal<Pagamento[]>([]);
  readonly paginaEmpenhos = signal(0);
  readonly paginaLiquidacoes = signal(0);
  readonly paginaPagamentos = signal(0);
  readonly tipoAtivo = signal<TipoDespesa>('empenho');
  readonly carregandoResumo = signal(false);
  readonly carregandoTabela = signal(false);
  readonly erro = signal('');
  readonly modalAberto = signal(false);
  readonly itemSelecionado = signal<RegistroDespesa | null>(null);
  readonly tipoModal = signal<TipoDespesa | null>(null);
  readonly tamanho = 10;
  private carregados = new Set<TipoDespesa>();

  constructor(private readonly api: ApiService) {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['cnpj'] && this.cnpj) this.reiniciar();
  }

  @HostListener('document:keydown.escape')
  fecharComEscape(): void {
    if (this.modalAberto()) this.fechar();
  }

  selecionarTipo(tipo: TipoDespesa): void {
    this.tipoAtivo.set(tipo);
    if (!this.carregados.has(tipo)) this.carregarTabela(tipo);
  }

  mudarPagina(pagina: number): void {
    if (pagina < 0) return;
    const tipo = this.tipoAtivo();
    if (tipo === 'empenho') this.paginaEmpenhos.set(pagina);
    if (tipo === 'liquidacao') this.paginaLiquidacoes.set(pagina);
    if (tipo === 'pagamento') this.paginaPagamentos.set(pagina);
    this.carregarTabela(tipo);
  }

  total(tipo: TipoDespesa): number {
    const chave =
      tipo === 'empenho' ? 'empenhos' : tipo === 'liquidacao' ? 'liquidacoes' : 'pagamentos';
    return this.resumo()?.[chave]?.total ?? 0;
  }

  soma(tipo: TipoDespesa): number {
    const chave =
      tipo === 'empenho' ? 'empenhos' : tipo === 'liquidacao' ? 'liquidacoes' : 'pagamentos';
    return Number(this.resumo()?.[chave]?.soma ?? 0);
  }

  totalPaginas(): number {
    return Math.ceil(this.total(this.tipoAtivo()) / this.tamanho);
  }

  get empenhoSelecionado(): Empenho | null {
    return this.tipoModal() === 'empenho' ? (this.itemSelecionado() as Empenho) : null;
  }

  get liquidacaoSelecionada(): Liquidacao | null {
    return this.tipoModal() === 'liquidacao' ? (this.itemSelecionado() as Liquidacao) : null;
  }

  get pagamentoSelecionado(): Pagamento | null {
    return this.tipoModal() === 'pagamento' ? (this.itemSelecionado() as Pagamento) : null;
  }

  paginaAtual(): number {
    if (this.tipoAtivo() === 'empenho') return this.paginaEmpenhos();
    if (this.tipoAtivo() === 'liquidacao') return this.paginaLiquidacoes();
    return this.paginaPagamentos();
  }

  abrirModal(item: RegistroDespesa, tipo: TipoDespesa): void {
    this.itemSelecionado.set(item);
    this.tipoModal.set(tipo);
    this.modalAberto.set(true);
  }

  fechar(): void {
    this.modalAberto.set(false);
    this.itemSelecionado.set(null);
    this.tipoModal.set(null);
  }

  tentarNovamente(): void {
    this.carregarTabela(this.tipoAtivo());
  }

  private reiniciar(): void {
    this.resumo.set(null);
    this.empenhos.set([]);
    this.liquidacoes.set([]);
    this.pagamentos.set([]);
    this.paginaEmpenhos.set(0);
    this.paginaLiquidacoes.set(0);
    this.paginaPagamentos.set(0);
    this.tipoAtivo.set('empenho');
    this.carregados.clear();
    this.erro.set('');
    this.fechar();
    this.carregarResumo();
    this.carregarTabela('empenho');
  }

  private carregarResumo(): void {
    this.carregandoResumo.set(true);
    this.api
      .buscarResumoDespesas(this.cnpj)
      .pipe(finalize(() => this.carregandoResumo.set(false)))
      .subscribe({
        next: (resumo) => this.resumo.set(resumo),
        error: (error) =>
          this.erro.set(
            this.api.mensagemErro(error, 'Não foi possível carregar o resumo financeiro.'),
          ),
      });
  }

  private carregarTabela(tipo: TipoDespesa): void {
    this.carregandoTabela.set(true);
    this.erro.set('');
    const pagina =
      tipo === 'empenho'
        ? this.paginaEmpenhos()
        : tipo === 'liquidacao'
          ? this.paginaLiquidacoes()
          : this.paginaPagamentos();
    const falhar = (error: unknown) =>
      this.erro.set(this.api.mensagemErro(error, 'Não foi possível carregar os registros.'));

    if (tipo === 'empenho') {
      this.api
        .buscarEmpenhos(this.cnpj, pagina)
        .pipe(finalize(() => this.carregandoTabela.set(false)))
        .subscribe({
          next: (itens) => {
            this.empenhos.set(itens);
            this.carregados.add(tipo);
          },
          error: falhar,
        });
    } else if (tipo === 'liquidacao') {
      this.api
        .buscarLiquidacoes(this.cnpj, pagina)
        .pipe(finalize(() => this.carregandoTabela.set(false)))
        .subscribe({
          next: (itens) => {
            this.liquidacoes.set(itens);
            this.carregados.add(tipo);
          },
          error: falhar,
        });
    } else {
      this.api
        .buscarPagamentos(this.cnpj, pagina)
        .pipe(finalize(() => this.carregandoTabela.set(false)))
        .subscribe({
          next: (itens) => {
            this.pagamentos.set(itens);
            this.carregados.add(tipo);
          },
          error: falhar,
        });
    }
  }
}
