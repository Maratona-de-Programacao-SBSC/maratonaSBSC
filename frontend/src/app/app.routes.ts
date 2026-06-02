import { Routes } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { NotasComponent } from './notas/notas.component';
import { DespesasComponent } from './despesas/despesas.component';

export const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'notas', component: NotasComponent },
  { path: 'despesas', component: DespesasComponent },
];