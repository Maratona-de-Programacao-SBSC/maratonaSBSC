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
import { ItemNotaFiscal, NotaFiscal } from '../../models/api.models';
import { PaginationComponent } from '../ui/pagination/pagination';

@Component({
  selector: 'app-notas',
  standalone: true,
  imports: [CommonModule, PaginationComponent],
  templateUrl: './notas.html',
  styleUrl: './notas.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class NotasComponent implements OnChanges {
  @Input() cnpj = '';

  readonly notas = signal<NotaFiscal[]>([]);
  readonly pagina = signal(0);
  readonly totalPaginas = signal(0);
  readonly total = signal(0);
  readonly loading = signal(false);
  readonly erro = signal('');
  readonly modalAberto = signal(false);
  readonly notaSelecionada = signal<NotaFiscal | null>(null);
  readonly itens = signal<ItemNotaFiscal[]>([]);
  readonly loadingItens = signal(false);
  readonly erroItens = signal('');

  constructor(private readonly api: ApiService) {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['cnpj'] && this.cnpj) {
      this.pagina.set(0);
      this.fechar();
      this.carregarNotas();
    }
  }

  @HostListener('document:keydown.escape')
  fecharComEscape(): void {
    if (this.modalAberto()) this.fechar();
  }

  mudarPagina(pagina: number): void {
    if (pagina < 0 || pagina >= this.totalPaginas()) return;
    this.pagina.set(pagina);
    this.carregarNotas();
  }

  abrirNota(nota: NotaFiscal): void {
    this.notaSelecionada.set(nota);
    this.itens.set([]);
    this.erroItens.set('');
    this.loadingItens.set(true);
    this.modalAberto.set(true);

    this.api
      .buscarItensNota(this.cnpj, nota.chave_acesso)
      .pipe(finalize(() => this.loadingItens.set(false)))
      .subscribe({
        next: (itens) => this.itens.set(itens),
        error: (error) =>
          this.erroItens.set(
            this.api.mensagemErro(error, 'Não foi possível carregar os itens da nota.'),
          ),
      });
  }

  fechar(): void {
    this.modalAberto.set(false);
    this.notaSelecionada.set(null);
    this.itens.set([]);
    this.erroItens.set('');
  }

  carregarNotas(): void {
    this.loading.set(true);
    this.erro.set('');
    this.api
      .buscarNotas(this.cnpj, this.pagina())
      .pipe(finalize(() => this.loading.set(false)))
      .subscribe({
        next: (resposta) => {
          this.notas.set(resposta.notas);
          this.total.set(resposta.total);
          this.totalPaginas.set(resposta.total_paginas);
        },
        error: (error) =>
          this.erro.set(
            this.api.mensagemErro(error, 'Não foi possível carregar as notas fiscais.'),
          ),
      });
  }
}
