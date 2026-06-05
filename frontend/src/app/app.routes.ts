import { Routes } from '@angular/router';
import { Main } from './pages/main/main';
import { ConsultasComponent } from './pages/consulta/consulta';

export const routes: Routes = [
  {
    path: '',
    component: Main
  },
  {
    path: 'dashboard',
    component: ConsultasComponent  
  }
];