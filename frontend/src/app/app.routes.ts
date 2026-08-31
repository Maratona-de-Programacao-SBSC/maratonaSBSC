import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    title: 'Ágoradit — Transparência pública',
    loadComponent: () => import('./pages/main/main').then((module) => module.Main),
  },
  {
    path: 'dashboard',
    title: 'Consultar fornecedor — Ágoradit',
    loadComponent: () =>
      import('./pages/consulta/consulta').then((module) => module.ConsultasComponent),
  },
  {
    path: 'ranking',
    title: 'Alertas da comunidade — Ágoradit',
    loadComponent: () =>
      import('./pages/ranking/ranking').then((module) => module.RankingComponent),
  },
  { path: '**', redirectTo: '' },
];
