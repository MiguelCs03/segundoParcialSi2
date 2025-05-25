import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { SessionService } from '../services/session.service';

export function roleGuard(allowedRoles: string[]): CanActivateFn {
  return () => {
    const session = inject(SessionService);
    const router = inject(Router);

    const rol = session.role;

    if (session.isLoggedIn && rol && allowedRoles.includes(rol)) {

      return true;
    }

    return router.createUrlTree(['/no-autorizado']);
  };
}
