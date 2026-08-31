import { ChangeDetectionStrategy, Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Subscription, distinctUntilChanged, finalize, map } from 'rxjs';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

import { ApiService } from '../../services/api';
import { EmpresaLocal } from '../../models/api.models';
import { DespesasComponent } from '../../components/despesas/despesas';
import { NotasComponent } from '../../components/notas/notas';
import { InfosComponent } from '../../components/infos/infos';
import { VotoComponent } from '../../components/voto/voto';

type AbaConsulta = 'despesas' | 'notas';

@Component({
  selector: 'app-consultas',
  standalone: true,
  imports: [CommonModule, FormsModule, DespesasComponent, NotasComponent, InfosComponent, VotoComponent],
  templateUrl: './consulta.html',
  styleUrls: ['./consulta.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ConsultasComponent implements OnInit {
  private readonly api = inject(ApiService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly destroyRef = inject(DestroyRef);
  private consultaAtual?: Subscription;

  cnpjInput = '';
  readonly cnpjConsultado = signal('');
  readonly empresa = signal<EmpresaLocal | null>(null);
  readonly loading = signal(false);
  readonly erro = signal('');
  readonly aba = signal<AbaConsulta>('despesas');

  ngOnInit(): void {
    this.route.queryParamMap
      .pipe(
        map((params) => (params.get('cnpj') ?? '').replace(/\D/g, '')),
        distinctUntilChanged(),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe((cnpj) => {
        if (cnpj.length === 14) {
          this.cnpjInput = this.formatarCnpj(cnpj);
          this.consultar(cnpj);
        }
      });
  }

  atualizarEntrada(valor: string): void {
    this.cnpjInput = this.formatarCnpj(valor);
    if (this.erro()) this.erro.set('');
  }

  pesquisar(): void {
    const cnpj = this.somenteDigitos(this.cnpjInput);
    if (cnpj.length !== 14) {
      this.erro.set('Digite os 14 números do CNPJ para continuar.');
      return;
    }

    if (cnpj === this.cnpjConsultado()) {
      this.consultar(cnpj);
      return;
    }

    void this.router.navigate([], {
      relativeTo: this.route,
      queryParams: { cnpj },
      queryParamsHandling: 'merge',
    });
  }

  selecionarAba(aba: AbaConsulta): void {
    this.aba.set(aba);
  }

  tentarNovamente(): void {
    const cnpj = this.somenteDigitos(this.cnpjInput);
    if (cnpj.length === 14) this.consultar(cnpj);
  }

  formatarCnpj(valor: string): string {
    const digitos = this.somenteDigitos(valor).slice(0, 14);
    return digitos
      .replace(/^(\d{2})(\d)/, '$1.$2')
      .replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3')
      .replace(/\.(\d{3})(\d)/, '.$1/$2')
      .replace(/(\d{4})(\d)/, '$1-$2');
  }

  private consultar(cnpj: string): void {
    this.consultaAtual?.unsubscribe();
    this.loading.set(true);
    this.erro.set('');
    this.empresa.set(null);
    this.cnpjConsultado.set('');
    this.aba.set('despesas');

    this.consultaAtual = this.api
      .buscarInformacoes(cnpj)
      .pipe(finalize(() => this.loading.set(false)))
      .subscribe({
        next: (empresa) => {
          this.empresa.set(empresa);
          this.cnpjConsultado.set(cnpj);
        },
        error: (error) => this.erro.set(this.api.mensagemErro(error)),
      });
  }

  private somenteDigitos(valor: string): string {
    return valor.replace(/\D/g, '');
  }
}
