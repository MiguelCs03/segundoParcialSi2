import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';
import { roleGuard } from './core/guards/role.guard';

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
  canActivate: [authGuard, roleGuard(['profesor'])],
  loadComponent: () =>
    import('./modules/dashboard/pages/profesor-dashboard.component').then(m => m.ProfesorDashboardComponent)
  },
  {
  path: 'profesor/materia/:id',
  canActivate: [authGuard, roleGuard(['profesor'])],
  loadComponent: () =>
    import('./modules/dashboard/pages/materia-detalle.component').then(m => m.MateriaDetalleComponent)
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
  {
     path: 'no-autorizado',
    loadComponent: () => import('./shared/pages/no-autorizado.component').then(m => m.NoAutorizadoComponent)
  }
];

