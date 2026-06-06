import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api';

export interface CnpjSuspeito {
  cnpj: string;
  razao_social: string;
  votos_cidadaos: number;
}

@Component({
  selector: 'app-ranking-table',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './ranking-table.html',
  styleUrls: ['./ranking-table.scss']
})
export class RankingTableComponent implements OnInit {

  top5: CnpjSuspeito[] = [];
  loading = false;

  constructor(
    private api: ApiService,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.carregar();
  }

  async carregar() {
    this.loading = true;
    this.cdr.detectChanges();

    this.api.buscarRanking().subscribe({
      next: async (res: any) => {
        this.top5 = res;
        this.loading = false;
        this.cdr.detectChanges();

        for (let i = 0; i < this.top5.length; i++) {
          const item = this.top5[i];

          // verifica localStorage primeiro
          if (this.api.temInfosExternas(item.cnpj)) {
            item.razao_social = this.api.getNomeCache(item.cnpj) ?? item.cnpj;
            this.cdr.detectChanges();
            continue;
          }

          if (item.razao_social) continue;

          await new Promise(r => setTimeout(r, 300 * i));

          this.api.buscarInfosExternas(item.cnpj).subscribe({
            next: (info: any) => {
              item.razao_social = info.razao_social ?? item.cnpj;
              this.cdr.detectChanges();
            },
            error: () => {
              item.razao_social = item.cnpj;
              this.cdr.detectChanges();
            }
          });
        }
      },
      error: () => {
        this.loading = false;
        this.cdr.detectChanges();
      }
    });
  }

  irParaDashboard(cnpj: string) {
    this.router.navigate(['/dashboard'], { queryParams: { cnpj } });
  }
}