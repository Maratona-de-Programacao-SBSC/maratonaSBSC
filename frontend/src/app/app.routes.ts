import { Routes } from '@angular/router';
import { Main } from './pages/main/main';
import { ConsultasComponent } from './pages/consulta/consulta';
import { RankingComponent } from './pages/ranking/ranking'; // <-- Import da nova página!

export const routes: Routes = [
  {
    path: '',
    component: Main
  },
  {
    path: 'dashboard',
    component: ConsultasComponent  
  },
  { 
    path: 'ranking', 
    component: RankingComponent
  }
];