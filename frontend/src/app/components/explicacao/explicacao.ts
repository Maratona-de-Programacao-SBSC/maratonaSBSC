import { ChangeDetectionStrategy, Component, signal } from '@angular/core';

type Secao = 'empenho' | 'liquidacao' | 'notas' | 'pagamento';

@Component({
  selector: 'app-explicacao',
  templateUrl: './explicacao.html',
  styleUrls: ['./explicacao.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ExplicacoesComponent {
  readonly aberto = signal<Secao | null>('empenho');

  toggle(secao: Secao): void {
    this.aberto.update((atual) => (atual === secao ? null : secao));
  }
}
