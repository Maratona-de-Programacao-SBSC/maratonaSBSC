import { Component, Input, ChangeDetectorRef, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-despesas',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './despesas.html',
  styleUrls: ['./despesas.scss']
})
export class DespesasComponent implements OnChanges {

  @Input() resultado: any;

  constructor(private cdr: ChangeDetectorRef) {}

  ngOnChanges(changes: SimpleChanges) {
    if (changes['resultado']) {
      this.cdr.detectChanges();
    }
  }

  get totalEmpenhado(): number {
    return (this.resultado?.empenhos || [])
      .reduce((soma: number, item: any) => soma + Number(item.valor || 0), 0);
  }

  get totalPago(): number {
    return (this.resultado?.pagamentos || [])
      .reduce((soma: number, item: any) => soma + Number(item.valor || 0), 0);
  }
}