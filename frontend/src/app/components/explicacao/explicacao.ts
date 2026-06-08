import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-explicacao',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './explicacao.html',
  styleUrls: ['./explicacao.scss']
})
export class ExplicacoesComponent {
  aberto: string | null = null;

  toggle(secao: string) {
    this.aberto = this.aberto === secao ? null : secao;
  }
}