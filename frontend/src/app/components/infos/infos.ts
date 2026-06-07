import { Component, Input, OnChanges, SimpleChanges, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-infos',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './infos.html',
  styleUrl: './infos.scss'
})
export class InfosComponent implements OnChanges {

  @Input() cnpj = '';

  dados: any = null;
  loading = false;
  erro = false;
  mapUrl: SafeResourceUrl | null = null;

  constructor(
    private api: ApiService,
    private cdr: ChangeDetectorRef,
    private sanitizer: DomSanitizer
  ) {}

  ngOnChanges(changes: SimpleChanges) {
    if (changes['cnpj'] && this.cnpj) {
      this.carregar();
    }
  }

  carregar() {
    this.loading = true;
    this.erro = false;
    this.dados = null;
    this.mapUrl = null;

    this.api.buscarInfosExternas(this.cnpj).subscribe({
      next: (res) => {
        this.dados = res;
        this.mapUrl = this.gerarMapUrl(res);
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: () => {
        this.erro = true;
        this.loading = false;
        this.cdr.detectChanges();
      }
    });
  }

  private gerarMapUrl(dados: any): SafeResourceUrl {
    const partes = [
      dados.descricao_tipo_de_logradouro,
      dados.logradouro,
      dados.numero,
      dados.bairro,
      dados.municipio,
      dados.uf,
      'Brasil'
    ].filter(Boolean);
    const query = encodeURIComponent(partes.join(' '));
    return this.sanitizer.bypassSecurityTrustResourceUrl(
      `https://maps.google.com/maps?q=${query}&output=embed`
    );
  }
}