import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

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

  dadosOriginais: CnpjSuspeito[] = [
    { cnpj: '05340639000130', razao_social: 'EMPRESA FANTASMA S.A.', votos_cidadaos: 23 },
    { cnpj: '12345678000199', razao_social: 'COMÉRCIO DE FACHADA LTDA', votos_cidadaos: 20 },
    { cnpj: '98765432000111', razao_social: 'SERVIÇOS GERAIS EIRELI', votos_cidadaos: 15 },
    { cnpj: '11222333000144', razao_social: 'CONSTRUTORA DE PAPEL', votos_cidadaos: 11 },
    { cnpj: '55666777000188', razao_social: 'LARANJA & CIA', votos_cidadaos: 10 },
    { cnpj: '99888777000166', razao_social: 'TECNOLOGIA INEXISTENTE', votos_cidadaos: 8 },
    { cnpj: '33444555000122', razao_social: 'CONSULTORIA FAKE', votos_cidadaos: 7 },
    { cnpj: '77888999000133', razao_social: 'IMPORTADORA DE NADA', votos_cidadaos: 5 },
    { cnpj: '10203040000155', razao_social: 'DISTRIBUIDORA SUSPEITA', votos_cidadaos: 3 },
    { cnpj: '50607080000199', razao_social: 'LIMPEZA E CONSERVAÇÃO ME', votos_cidadaos: 2 },
    { cnpj: '11122233000100', razao_social: 'EMPRESA FORA DO TOP 10', votos_cidadaos: 1 }
  ];

  top10: CnpjSuspeito[] = [];

  ngOnInit() {
    // Apenas ordena e pega os 10 primeiros
    this.dadosOriginais.sort((a, b) => b.votos_cidadaos - a.votos_cidadaos);
    this.top10 = this.dadosOriginais.slice(0, 10);
  }
}