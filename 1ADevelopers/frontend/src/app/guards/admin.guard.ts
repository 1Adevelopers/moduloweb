import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';

export const adminGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const token = localStorage.getItem('access_token');
  const userString = localStorage.getItem('user');

  if (!token || !userString) {
    router.navigate(['/login']);
    return false;
  }

  try {
    const user = JSON.parse(userString);

    if (user.rol === 1 || user.rol?.id === 1) {
      return true; // ¡Acceso concedido!
    }
  } catch (e) {
    console.error('Error al procesar los datos del usuario en el Guard', e);
  }

  router.navigate(['/home']);
  return false;
};
