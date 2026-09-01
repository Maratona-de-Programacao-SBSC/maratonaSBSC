import {
  ChangeDetectionStrategy,
  Component,
  Input,
  OnChanges,
  SimpleChanges,
  signal,
} from '@angular/core';
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-voto',
  standalone: true,
  templateUrl: './voto.html',
  styleUrl: './voto.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class VotoComponent implements OnChanges {
  @Input() cnpj = '';

  readonly votos = signal(0);
  readonly jaVotou = signal(false);
  readonly loading = signal(false);
  readonly confirmando = signal(false);
  readonly erro = signal('');

  constructor(private readonly api: ApiService) {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['cnpj'] && this.cnpj) {
      this.jaVotou.set(this.lerVotoLocal());
      this.confirmando.set(false);
      this.erro.set('');
      this.carregar();
    }
  }

  iniciarConfirmacao(): void {
    if (!this.jaVotou()) this.confirmando.set(true);
  }

  cancelar(): void {
    this.confirmando.set(false);
  }

  votar(): void {
    if (this.jaVotou() || this.loading()) return;
    this.loading.set(true);
    this.erro.set('');

    this.api.votar(this.cnpj).subscribe({
      next: (avaliacao) => {
        this.votos.set(avaliacao.votos_cidadaos ?? 0);
        this.jaVotou.set(true);
        this.confirmando.set(false);
        this.loading.set(false);
        this.salvarVotoLocal();
      },
      error: (error) => {
        this.erro.set(this.api.mensagemErro(error, 'Não foi possível registrar o alerta.'));
        this.loading.set(false);
      },
    });
  }

  private carregar(): void {
    this.api.buscarAvaliacao(this.cnpj).subscribe({
      next: (avaliacao) => this.votos.set(avaliacao.votos_cidadaos ?? 0),
      error: () => this.erro.set('Não foi possível carregar os alertas.'),
    });
  }

  private lerVotoLocal(): boolean {
    try {
      return localStorage.getItem(`voto_${this.cnpj}`) === 'true';
    } catch {
      return false;
    }
  }

  private salvarVotoLocal(): void {
    try {
      localStorage.setItem(`voto_${this.cnpj}`, 'true');
    } catch {
      // O bloqueio do armazenamento local não impede o registro no servidor.
    }
  }
}
