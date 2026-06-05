import { Routes } from '@angular/router';
import { DashboardComponent } from './pages/dashboard/dashboard';
import { Main } from './pages/main/main';

export const routes: Routes = [
  {
    path: '',
    component: Main
  },
  {
    path: 'dashboard',
    component: DashboardComponent
  }
];