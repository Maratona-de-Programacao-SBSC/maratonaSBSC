import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-despesas',
  standalone: true,
  imports: [],
  templateUrl: './despesas.html',
  styleUrls: ['./despesas.scss']
})
export class DespesasComponent {

  @Input() resultado: any;

  get totalEmpenhado(): number {
    return (this.resultado?.empenhos || [])
      .reduce((soma: number, item: any) => soma + Number(item.valor || 0), 0);
  }

  get totalPago(): number {
    return (this.resultado?.pagamentos || [])
      .reduce((soma: number, item: any) => soma + Number(item.valor || 0), 0);
  }
}