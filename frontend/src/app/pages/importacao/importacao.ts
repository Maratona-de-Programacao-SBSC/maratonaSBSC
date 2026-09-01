import { CommonModule } from '@angular/common';
import {
  ChangeDetectionStrategy,
  Component,
  DestroyRef,
  computed,
  inject,
  signal,
} from '@angular/core';
import { FormsModule } from '@angular/forms';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Subscription, finalize, switchMap, takeWhile, timer } from 'rxjs';

import { JobImportacao, PeriodoImportacao, TipoImportacao } from '../../models/api.models';
import { ApiService } from '../../services/api';

interface OpcaoImportacao {
  tipo: TipoImportacao;
  titulo: string;
  descricao: string;
  limiteDias?: number;
}

const STATUS_FINAIS = new Set(['SUCCESS', 'FAILURE', 'REVOKED']);

@Component({
  selector: 'app-importacao',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './importacao.html',
  styleUrl: './importacao.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ImportacaoComponent {
  private readonly api = inject(ApiService);
  private readonly destroyRef = inject(DestroyRef);
  private acompanhamentoAtual?: Subscription;

  readonly opcoes: OpcaoImportacao[] = [
    {
      tipo: 'despesas',
      titulo: 'Despesas públicas',
      descricao: 'Importa empenhos, liquidações e pagamentos do período.',
      limiteDias: 366,
    },
    {
      tipo: 'notas',
      titulo: 'Notas fiscais',
      descricao: 'Atualiza os documentos fiscais emitidos no período.',
      limiteDias: 3660,
    },
    {
      tipo: 'itens-notas',
      titulo: 'Itens das notas',
      descricao: 'Importa os produtos e serviços detalhados nas notas.',
      limiteDias: 3660,
    },
    {
      tipo: 'cnpj',
      titulo: 'Base de CNPJs',
      descricao: 'Atualiza a base completa de empresas. Esta carga pode ser demorada.',
    },
  ];

  chaveAdministrativa = '';
  dataInicio = this.dataDiasAtras(29);
  dataFim = this.dataDiasAtras(0);
  confirmacaoCargaCompleta = false;

  readonly tipo = signal<TipoImportacao>('despesas');
  readonly mostrarChave = signal(false);
  readonly enviando = signal(false);
  readonly erro = signal('');
  readonly job = signal<JobImportacao | null>(null);
  readonly hoje = this.dataDiasAtras(0);
  readonly opcaoAtual = computed(() => this.opcoes.find((opcao) => opcao.tipo === this.tipo())!);
  readonly resultado = computed(() => {
    const dados = this.job()?.resultado;
    if (!dados) return [];
    return Object.entries(dados).map(([chave, valor]) => ({
      chave: this.formatarRotulo(chave),
      valor: typeof valor === 'object' ? JSON.stringify(valor) : String(valor),
    }));
  });

  selecionarTipo(tipo: TipoImportacao): void {
    this.tipo.set(tipo);
    this.confirmacaoCargaCompleta = false;
    this.erro.set('');
  }

  alternarVisibilidadeChave(): void {
    this.mostrarChave.update((visivel) => !visivel);
  }

  iniciar(): void {
    const validacao = this.validarFormulario();
    if (validacao) {
      this.erro.set(validacao);
      return;
    }

    const chave = this.chaveAdministrativa.trim();
    const periodo: PeriodoImportacao | undefined =
      this.tipo() === 'cnpj' ? undefined : { dataInicio: this.dataInicio, dataFim: this.dataFim };

    this.acompanhamentoAtual?.unsubscribe();
    this.erro.set('');
    this.job.set(null);
    this.enviando.set(true);

    this.api
      .iniciarImportacao(this.tipo(), chave, periodo)
      .pipe(finalize(() => this.enviando.set(false)))
      .subscribe({
        next: (jobCriado) => {
          this.job.set({ ...jobCriado, resultado: null });
          this.acompanhar(jobCriado.job_id, chave);
        },
        error: (error) =>
          this.erro.set(this.api.mensagemErro(error, 'Não foi possível iniciar a importação.')),
      });
  }

  novaImportacao(): void {
    this.acompanhamentoAtual?.unsubscribe();
    this.job.set(null);
    this.erro.set('');
    this.confirmacaoCargaCompleta = false;
  }

  statusTraduzido(status: string): string {
    const rotulos: Record<string, string> = {
      PENDING: 'Na fila',
      STARTED: 'Em andamento',
      RETRY: 'Tentando novamente',
      SUCCESS: 'Concluída',
      FAILURE: 'Falhou',
      REVOKED: 'Cancelada',
    };
    return rotulos[status] ?? status;
  }

  statusClasse(status: string): string {
    if (status === 'SUCCESS') return 'success';
    if (status === 'FAILURE' || status === 'REVOKED') return 'danger';
    return 'progress';
  }

  private acompanhar(jobId: string, chaveAdministrativa: string): void {
    this.acompanhamentoAtual = timer(1000, 3000)
      .pipe(
        switchMap(() => this.api.consultarImportacao(jobId, chaveAdministrativa)),
        takeWhile((job) => !STATUS_FINAIS.has(job.status), true),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe({
        next: (job) => this.job.set(job),
        error: (error) =>
          this.erro.set(
            this.api.mensagemErro(
              error,
              'A importação foi iniciada, mas o status não pôde ser atualizado.',
            ),
          ),
      });
  }

  private validarFormulario(): string {
    if (!this.chaveAdministrativa.trim()) return 'Informe a chave administrativa para continuar.';

    if (this.tipo() === 'cnpj') {
      return this.confirmacaoCargaCompleta
        ? ''
        : 'Confirme que está ciente de que a carga completa pode ser demorada.';
    }

    if (!this.dataInicio || !this.dataFim) return 'Informe as datas inicial e final.';
    if (this.dataFim > this.hoje) return 'A data final não pode estar no futuro.';
    if (this.dataInicio > this.dataFim) return 'A data inicial deve ser anterior à data final.';

    const limite = this.opcaoAtual().limiteDias;
    const dias = this.diferencaEmDias(this.dataInicio, this.dataFim);
    if (limite !== undefined && dias > limite) {
      return `O período máximo para esta carga é de ${limite} dias.`;
    }

    return '';
  }

  private diferencaEmDias(inicio: string, fim: string): number {
    const milissegundosPorDia = 24 * 60 * 60 * 1000;
    return Math.floor(
      (Date.parse(`${fim}T00:00:00Z`) - Date.parse(`${inicio}T00:00:00Z`)) / milissegundosPorDia,
    );
  }

  private dataDiasAtras(dias: number): string {
    const data = new Date();
    data.setHours(12, 0, 0, 0);
    data.setDate(data.getDate() - dias);
    const ano = data.getFullYear();
    const mes = String(data.getMonth() + 1).padStart(2, '0');
    const dia = String(data.getDate()).padStart(2, '0');
    return `${ano}-${mes}-${dia}`;
  }

  private formatarRotulo(valor: string): string {
    const texto = valor.replaceAll('_', ' ');
    return texto.charAt(0).toUpperCase() + texto.slice(1);
  }
}
