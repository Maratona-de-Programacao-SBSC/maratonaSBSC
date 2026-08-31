import { ChangeDetectionStrategy, Component, OnInit, computed, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { finalize } from 'rxjs';
import { ApiService } from '../../services/api';
import { CnpjSuspeito } from '../../models/api.models';

type NivelAlerta = 'Crítico' | 'Alto' | 'Atenção' | 'Observação';

@Component({
  selector: 'app-ranking-table',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './ranking-table.html',
  styleUrls: ['./ranking-table.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class RankingTableComponent implements OnInit {
  readonly ranking = signal<CnpjSuspeito[]>([]);
  readonly loading = signal(false);
  readonly erro = signal('');
  readonly maiorVotacao = computed(() => Math.max(...this.ranking().map((item) => item.votos_cidadaos), 1));

  constructor(private readonly api: ApiService) {}

  ngOnInit(): void {
    this.carregar();
  }

  carregar(): void {
    this.loading.set(true);
    this.erro.set('');
    this.api.buscarRanking(10).pipe(finalize(() => this.loading.set(false))).subscribe({
      next: (ranking) => this.ranking.set(ranking),
      error: (error) => this.erro.set(this.api.mensagemErro(error, 'Não foi possível carregar os alertas da comunidade.')),
    });
  }

  nivel(votos: number): NivelAlerta {
    if (votos >= 20) return 'Crítico';
    if (votos >= 10) return 'Alto';
    if (votos >= 5) return 'Atenção';
    return 'Observação';
  }

  classeNivel(votos: number): string {
    if (votos >= 20) return 'critical';
    if (votos >= 10) return 'high';
    if (votos >= 5) return 'medium';
    return 'low';
  }

  percentual(votos: number): number {
    return Math.max(4, Math.round((votos / this.maiorVotacao()) * 100));
  }

  formatarCnpj(cnpj: string): string {
    return cnpj.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/, '$1.$2.$3/$4-$5');
  }
}
