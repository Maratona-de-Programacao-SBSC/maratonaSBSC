import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';

@Component({
  selector: 'app-pagination',
  templateUrl: './pagination.html',
  styleUrl: './pagination.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PaginationComponent {
  readonly pagina = input.required<number>();
  readonly totalPaginas = input.required<number>();
  readonly paginaChange = output<number>();

  anterior(): void {
    if (this.pagina() > 0) this.paginaChange.emit(this.pagina() - 1);
  }

  proxima(): void {
    if (this.pagina() < this.totalPaginas() - 1) this.paginaChange.emit(this.pagina() + 1);
  }
}
