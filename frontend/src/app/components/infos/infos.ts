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

    this.api.buscarInfosExternas(this.cnpj).subscribe({
      next: (res) => {
        this.dados = res;
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

  get enderecoFormatado(): string {
    if (!this.dados) return '';
    const partes = [
      this.dados.descricao_tipo_de_logradouro,
      this.dados.logradouro,
      this.dados.numero,
      this.dados.bairro,
      this.dados.municipio,
      this.dados.uf,
      'Brasil'
    ].filter(Boolean);
    return encodeURIComponent(partes.join(' '));
  }

  get mapUrl(): SafeResourceUrl {
    const url = `https://maps.google.com/maps?q=${this.enderecoFormatado}&output=embed`;
    return this.sanitizer.bypassSecurityTrustResourceUrl(url);
  }
}