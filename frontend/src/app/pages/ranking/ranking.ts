import { Component } from '@angular/core';
// Importe o novo componente que acabamos de criar!
import { RankingTableComponent } from '../../components/ranking-table/ranking-table';

@Component({
  selector: 'app-ranking-page',
  standalone: true,
  // Coloque as peças de Lego aqui:
  imports: [RankingTableComponent], 
  templateUrl: './ranking.html'
})
export class RankingComponent {
  // A página em si não precisa de lógica nenhuma, ela só exibe os componentes!
}