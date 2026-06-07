import { Component, ViewChild, ElementRef, NgZone, ChangeDetectorRef, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';

import { ApiService } from '../../services/api';
import { DespesasComponent } from '../../components/despesas/despesas';
import { NotasComponent } from '../../components/notas/notas';
import { InfosComponent } from '../../components/infos/infos';
import { VotoComponent } from '../../components/voto/voto';

@Component({
  selector: 'app-consultas',
  standalone: true,
  imports: [CommonModule, FormsModule, DespesasComponent, NotasComponent, InfosComponent, VotoComponent],
  templateUrl: './consulta.html',
  styleUrls: ['./consulta.scss']
})
export class ConsultasComponent implements OnInit {

  @ViewChild('inputCnpj') inputCnpj!: ElementRef;

  cnpj = '';
  empresa: any = null;
  loading = false;
  aba: 'despesas' | 'notas' | 'outros' = 'despesas';

  constructor(
    private api: ApiService,
    private zone: NgZone,
    private cdr: ChangeDetectorRef,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      if (params['cnpj']) {
        this.cnpj = params['cnpj'];
        this.pesquisarPorCnpj(this.cnpj);
      }
    });
  }

  pesquisar() {
    const raw = this.inputCnpj.nativeElement.value.trim();
    this.cnpj = raw.replace(/\D/g, '');
    if (!this.cnpj) return;
    this.pesquisarPorCnpj(this.cnpj);
  }

  pesquisarPorCnpj(cnpj: string) {
    this.aba = 'despesas';
    this.empresa = null;
    this.loading = true;
    this.cdr.detectChanges();

    this.api.buscarInformacoes(cnpj).subscribe({
      next: (res) => {
        this.zone.run(() => {
          this.empresa = res;
          this.loading = false;
          this.cdr.detectChanges();
        });
      },
      error: () => {
        this.zone.run(() => {
          this.loading = false;
          this.cdr.detectChanges();
        });
      }
    });
  }
}