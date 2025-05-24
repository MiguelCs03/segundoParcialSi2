import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },

  {
    path: 'login',
    loadComponent: () =>
      import('./modules/auth/pages/login/login.component').then((m) => m.default),
  },

  // Sin guard ni componente hasta que existan
  {
    path: 'profesor',
    redirectTo: 'login',
    pathMatch: 'full',
  },
  {
    path: 'mi-rendimiento',
    redirectTo: 'login',
    pathMatch: 'full',
  },
  {
    path: 'mi-hijo',
    redirectTo: 'login',
    pathMatch: 'full',
  },
];

