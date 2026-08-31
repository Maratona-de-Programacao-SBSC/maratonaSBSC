import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RankingTableComponent } from '../../components/ranking-table/ranking-table';

@Component({
  selector: 'app-ranking-page',
  standalone: true,
  imports: [RankingTableComponent],
  templateUrl: './ranking.html',
  styleUrl: './ranking.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class RankingComponent {}
