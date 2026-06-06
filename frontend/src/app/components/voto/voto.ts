import { Component, Input, OnChanges, SimpleChanges, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-voto',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './voto.html',
  styleUrl: './voto.scss'
})
export class VotoComponent implements OnChanges {

  @Input() cnpj = '';

  votos = 0;
  jaVotou = false;
  loading = false;

  constructor(
    private api: ApiService,
    private cdr: ChangeDetectorRef
  ) {}

  carregar() {
    this.api.buscarAvaliacao(this.cnpj).subscribe({
      next: (res: any) => {
        this.votos = res.votos_cidadaos ?? 0;
        this.cdr.detectChanges();
      }
    });
  }

ngOnChanges(changes: SimpleChanges) {
  if (changes['cnpj'] && this.cnpj) {
    this.jaVotou = localStorage.getItem(`voto_${this.cnpj}`) === 'true';
    this.carregar();
  }
}

votar() {
  if (this.jaVotou || this.loading) return;

  this.loading = true;
  this.api.votar(this.cnpj).subscribe({
    next: (res: any) => {
      this.votos = res.votos_cidadaos ?? 0;
      this.jaVotou = true;
      this.loading = false;
      localStorage.setItem(`voto_${this.cnpj}`, 'true');
      this.cdr.detectChanges();
    },
    error: () => {
      this.loading = false;
      this.cdr.detectChanges();
    }
  });
}
}