import {
  ChangeDetectionStrategy,
  Component,
  Input,
  OnChanges,
  SimpleChanges,
  signal,
} from '@angular/core';
import { ApiService } from '../../services/api';
import { EmpresaBrasilApi } from '../../models/api.models';

@Component({
  selector: 'app-infos',
  standalone: true,
  templateUrl: './infos.html',
  styleUrl: './infos.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class InfosComponent implements OnChanges {
  @Input() cnpj = '';

  readonly dados = signal<EmpresaBrasilApi | null>(null);
  readonly loading = signal(false);
  readonly erro = signal(false);
  readonly mapUrl = signal('');

  constructor(private readonly api: ApiService) {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['cnpj'] && this.cnpj) this.carregar();
  }

  formatarCnpj(cnpj: string): string {
    return cnpj.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/, '$1.$2.$3/$4-$5');
  }

  private carregar(): void {
    this.loading.set(true);
    this.erro.set(false);
    this.dados.set(null);

    this.api.buscarInfosExternas(this.cnpj).subscribe({
      next: (dados) => {
        this.dados.set(dados);
        this.mapUrl.set(this.gerarMapUrl(dados));
        this.loading.set(false);
      },
      error: () => {
        this.erro.set(true);
        this.loading.set(false);
      },
    });
  }

  private gerarMapUrl(dados: EmpresaBrasilApi): string {
    const endereco = [
      dados.descricao_tipo_de_logradouro,
      dados.logradouro,
      dados.numero,
      dados.bairro,
      dados.municipio,
      dados.uf,
      'Brasil',
    ]
      .filter(Boolean)
      .join(' ');
    return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(endereco)}`;
  }
}
