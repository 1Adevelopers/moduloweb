import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';

export const authGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const token = localStorage.getItem('access_token');
  const userString = localStorage.getItem('user');

  // Si no hay token o no hay usuario guardado en el navegador (ej: modo incógnito)
  if (!token || !userString) {
    alert('Debe iniciar sesión para acceder a esta sección.');
    router.navigate(['/login']);
    return false;
  }

  return true; // Acceso permitido si la sesión existe
};
